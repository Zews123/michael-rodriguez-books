# SKILL: Gemini MCP Image Generation from CLI
**Role:** MCP Client Emulator  
**Mission:** Generate AI images via `gemini-webapi-mcp` server from any CLI environment (Copilot CLI, terminal, scripts) that lacks native MCP support.  
**Output:** PNG images in the project's `output/` directory

---

## PROBLEM STATEMENT

MCP (Model Context Protocol) servers are designed for **IDE clients** (VS Code, Cursor, Windsurf). These IDEs read `.vscode/mcp.json`, spawn the server process, and communicate via JSON-RPC over stdin/stdout automatically.

**Copilot CLI is NOT an MCP client.** It cannot read `mcp.json` or establish MCP connections natively. This skill documents how to **manually emulate an MCP client** using subprocess management and JSON-RPC protocol.

---

## PREREQUISITES

### Required tools
```bash
uv --version        # uv 0.5+ (Python package runner)
python3 --version   # Python 3.12+
```

### MCP server config location
```
/Users/zews/Book/.vscode/mcp.json
```

### Config format
```json
{
  "servers": {
    "gemini": {
      "command": "uv",
      "args": [
        "run", "--python", "3.12",
        "--with", "gemini-webapi-mcp[watermark] @ git+https://github.com/AndyShaman/gemini-webapi-mcp.git",
        "gemini-webapi-mcp"
      ]
    }
  }
}
```

### Authentication
- Uses **Chrome browser cookies** (not API key)
- User must be logged into Google/Gemini in Chrome
- Cookies expire — if auth fails, user must re-login in Chrome browser
- No environment variables or API keys needed

### Image output directory
```
/Users/zews/Pictures/gemini/
```
Server saves images here with timestamp filenames (e.g., `gemini_20260301_221500_abc123.png`).

---

## ARCHITECTURE

```
┌──────────────┐    stdin (JSON-RPC)     ┌──────────────────┐
│  CLI Agent   │ ──────────────────────► │  gemini-webapi-  │
│  (Copilot)   │ ◄────────────────────── │  mcp server      │
│              │    stdout (JSON-RPC)     │                  │
└──────────────┘                         └────────┬─────────┘
                                                  │
                                                  │ Chrome cookies
                                                  ▼
                                         ┌────────────────┐
                                         │  Gemini API    │
                                         │  (Google)      │
                                         └────────┬───────┘
                                                  │
                                                  ▼
                                         ┌────────────────┐
                                         │  PNG saved to  │
                                         │  ~/Pictures/   │
                                         │  gemini/       │
                                         └────────────────┘
```

---

## STAGE 1 — START MCP SERVER AS SUBPROCESS

Launch the server using the command from `mcp.json`:

```python
import subprocess
import json
import time
import os
import glob
import shutil

server_cmd = [
    "uv", "run", "--python", "3.12",
    "--with", "gemini-webapi-mcp[watermark] @ git+https://github.com/AndyShaman/gemini-webapi-mcp.git",
    "gemini-webapi-mcp"
]

proc = subprocess.Popen(
    server_cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=0    # Unbuffered — critical for JSON-RPC
)
```

> ⚠️ **Wait 12–15 seconds** after launch before sending any messages. The server needs time to:
> 1. Install/resolve dependencies (first run only)
> 2. Read Chrome cookies
> 3. Initialize Gemini session

```python
time.sleep(15)
```

---

## STAGE 2 — JSON-RPC HANDSHAKE

MCP uses JSON-RPC 2.0 over stdin/stdout. The handshake is mandatory — the server will reject tool calls without it.

### 2a. Send `initialize` request

```python
def send_jsonrpc(proc, method, params=None, msg_id=None):
    """Send a JSON-RPC message and optionally read the response."""
    msg = {"jsonrpc": "2.0", "method": method}
    if params:
        msg["params"] = params
    if msg_id is not None:
        msg["id"] = msg_id
    
    line = json.dumps(msg) + "\n"
    proc.stdin.write(line)
    proc.stdin.flush()
    
    if msg_id is not None:
        # Read response (blocking)
        response_line = proc.stdout.readline()
        return json.loads(response_line) if response_line else None
    return None


# Step 1: Initialize
init_response = send_jsonrpc(proc, "initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "copilot-cli", "version": "1.0.0"}
}, msg_id=1)

print("Server capabilities:", json.dumps(init_response, indent=2))
```

### 2b. Send `initialized` notification

```python
# Step 2: Confirm initialization (notification — no id, no response expected)
send_jsonrpc(proc, "notifications/initialized")
time.sleep(2)
```

> ⚠️ **Order matters:** `initialize` (request with id) → `notifications/initialized` (notification without id). Skipping or reordering will cause the server to ignore subsequent calls.

---

## STAGE 3 — GENERATE IMAGE

### 3a. Record existing files before generation

```python
GEMINI_DIR = os.path.expanduser("~/Pictures/gemini")
os.makedirs(GEMINI_DIR, exist_ok=True)

# Snapshot existing files BEFORE calling the tool
existing_files = set(glob.glob(os.path.join(GEMINI_DIR, "*.png")))
```

### 3b. Call `gemini_generate_image` tool

```python
prompt = """Create a dramatic book cover for 'Countdown to Collapse: The 2040 Crisis'.
A brutalist countdown clock against a deep red apocalyptic sky.
The clock hands point near midnight. Cracks spread across the clock face.
Dark, ominous atmosphere. Cinematic lighting. No text on the image.
Aspect ratio: portrait (2:3), suitable for book cover."""

response = send_jsonrpc(proc, "tools/call", {
    "name": "gemini_generate_image",
    "arguments": {"prompt": prompt}
}, msg_id=2)

print("Tool response:", json.dumps(response, indent=2))
```

### 3c. Monitor file system for new image

The server saves images to `~/Pictures/gemini/` asynchronously. Poll for new files:

```python
def wait_for_new_image(existing_files, gemini_dir, timeout=180, poll_interval=5):
    """Wait for a new PNG to appear in the Gemini output directory."""
    elapsed = 0
    while elapsed < timeout:
        current_files = set(glob.glob(os.path.join(gemini_dir, "*.png")))
        new_files = current_files - existing_files
        if new_files:
            # Return the newest file
            newest = max(new_files, key=os.path.getmtime)
            size_kb = os.path.getsize(newest) / 1024
            print(f"New image: {newest} ({size_kb:.0f} KB)")
            return newest
        time.sleep(poll_interval)
        elapsed += poll_interval
    
    raise TimeoutError(f"No new image after {timeout}s")


new_image = wait_for_new_image(existing_files, GEMINI_DIR)
```

### 3d. Copy to project directory

```python
project_output = "/Users/zews/Book/[Book_Name]/output/"
dest_name = "Cover_1_Concept_Name.png"
dest_path = os.path.join(project_output, dest_name)

shutil.copy2(new_image, dest_path)
print(f"Saved: {dest_path} ({os.path.getsize(dest_path) / 1024 / 1024:.1f} MB)")
```

---

## STAGE 4 — CLEANUP AND SERVER SHUTDOWN

```python
# Terminate the server process
proc.terminate()
try:
    proc.wait(timeout=5)
except subprocess.TimeoutExpired:
    proc.kill()

print("MCP server stopped.")
```

> ⚠️ **Start a fresh server for each image.** The cookie-based auth can become stale during long sessions, and Gemini may rate-limit sequential requests. A fresh process per image is more reliable.

---

## COMPLETE SINGLE-IMAGE SCRIPT

```python
#!/usr/bin/env python3
"""
Generate one image via Gemini MCP server.
Usage: python3 generate_cover.py "Your prompt here" output_filename.png
"""
import subprocess, json, time, os, glob, shutil, sys

GEMINI_DIR = os.path.expanduser("~/Pictures/gemini")
SERVER_CMD = [
    "uv", "run", "--python", "3.12",
    "--with", "gemini-webapi-mcp[watermark] @ git+https://github.com/AndyShaman/gemini-webapi-mcp.git",
    "gemini-webapi-mcp"
]

def send_msg(proc, method, params=None, msg_id=None):
    msg = {"jsonrpc": "2.0", "method": method}
    if params: msg["params"] = params
    if msg_id is not None: msg["id"] = msg_id
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
    if msg_id is not None:
        line = proc.stdout.readline()
        return json.loads(line) if line else None

def generate_image(prompt, output_path, timeout=180):
    os.makedirs(GEMINI_DIR, exist_ok=True)
    existing = set(glob.glob(os.path.join(GEMINI_DIR, "*.png")))
    
    # Start server
    proc = subprocess.Popen(SERVER_CMD,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, bufsize=0)
    
    try:
        print("Starting MCP server...")
        time.sleep(15)
        
        # Handshake
        send_msg(proc, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "copilot-cli", "version": "1.0.0"}
        }, msg_id=1)
        send_msg(proc, "notifications/initialized")
        time.sleep(2)
        
        # Generate
        print(f"Generating: {prompt[:80]}...")
        send_msg(proc, "tools/call", {
            "name": "gemini_generate_image",
            "arguments": {"prompt": prompt}
        }, msg_id=2)
        
        # Wait for file
        elapsed = 0
        while elapsed < timeout:
            current = set(glob.glob(os.path.join(GEMINI_DIR, "*.png")))
            new = current - existing
            if new:
                src = max(new, key=os.path.getmtime)
                shutil.copy2(src, output_path)
                size_mb = os.path.getsize(output_path) / 1024 / 1024
                print(f"✅ Saved: {output_path} ({size_mb:.1f} MB)")
                return output_path
            time.sleep(5)
            elapsed += 5
        
        raise TimeoutError(f"No image after {timeout}s")
    
    finally:
        proc.terminate()
        try: proc.wait(timeout=5)
        except: proc.kill()

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "A beautiful sunset over mountains"
    output = sys.argv[2] if len(sys.argv) > 2 else "output.png"
    generate_image(prompt, output)
```

---

## MULTI-IMAGE GENERATION (BOOK COVERS)

For generating multiple covers, loop with fresh server instances:

```python
covers = [
    {"prompt": "Brutalist clock, red sky...", "filename": "Cover_1_Clock.png"},
    {"prompt": "Burning hourglass...",        "filename": "Cover_2_Hourglass.png"},
    {"prompt": "Falling data graph...",       "filename": "Cover_3_Data.png"},
    {"prompt": "Split world...",              "filename": "Cover_4_Split.png"},
]

output_dir = "/Users/zews/Book/[Book_Name]/output/"

for i, cover in enumerate(covers, 1):
    print(f"\n{'='*50}")
    print(f"Generating cover {i}/{len(covers)}: {cover['filename']}")
    print(f"{'='*50}")
    
    output_path = os.path.join(output_dir, cover["filename"])
    generate_image(cover["prompt"], output_path)
    
    # Pause between generations to avoid rate limiting
    if i < len(covers):
        print("Waiting 10s before next generation...")
        time.sleep(10)

print(f"\n✅ All {len(covers)} covers generated!")
```

---

## COVER PROMPT BEST PRACTICES

| Rule | Why | Example |
|------|-----|---------|
| Always say "No text on the image" | Gemini adds random text/titles otherwise | `...cinematic lighting. No text on the image.` |
| Specify aspect ratio | Book covers need portrait 2:3 | `Aspect ratio: portrait (2:3)` |
| Describe mood, not just objects | Better artistic output | `Dark, ominous, tension` not just `a clock` |
| One focal element | Thumbnail readability | `A single hourglass` not `hourglass and clock and graph` |
| Mention "book cover" | Primes the model for cover composition | `Create a dramatic book cover for...` |
| Save prompts to JSON | Reproducibility for regeneration | `cover_prompts.json` alongside images |

---

## TROUBLESHOOTING

| Problem | Cause | Solution |
|---------|-------|----------|
| Server hangs on startup | Dependencies downloading (first run) | Wait 30–60s on first launch; 15s on subsequent |
| `initialize` returns nothing | Server not ready | Increase initial wait to 20–30s |
| Auth error / 401 | Chrome cookies expired | User must log into gemini.google.com in Chrome |
| Image not appearing | Gemini rate limit or content filter | Retry with modified prompt; wait 30s between tries |
| `tools/call` returns error | Wrong tool name | Use `tools/list` (msg_id=N) to discover available tools |
| Process zombie after error | `proc.terminate()` not called | Always use try/finally to clean up |
| Multiple images appear | Previous pending requests | Snapshot `existing_files` right before each call |
| Server crash mid-generation | Cookie session timeout | Restart server (fresh instance per image) |
| `uv` not found | Not installed or not in PATH | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Wrong Python version | Server needs 3.12 | `uv run --python 3.12` forces correct version |

---

## DISCOVERING MCP TOOLS

If you don't know what tools the server exposes, query them:

```python
tools_response = send_msg(proc, "tools/list", {}, msg_id=99)
for tool in tools_response.get("result", {}).get("tools", []):
    print(f"Tool: {tool['name']}")
    print(f"  Description: {tool.get('description', 'N/A')}")
    print(f"  Parameters: {json.dumps(tool.get('inputSchema', {}), indent=4)}")
```

Known tools for `gemini-webapi-mcp`:
- `gemini_generate_image` — generates image from text prompt
  - Input: `{"prompt": "string"}`
  - Output: image saved to `~/Pictures/gemini/`

---

## KEY LESSONS LEARNED

1. **Copilot CLI ≠ MCP client.** `.vscode/mcp.json` is for IDEs only. CLI must emulate the protocol manually.

2. **JSON-RPC handshake is mandatory.** `initialize` → `notifications/initialized` → then tool calls. Skip any step and the server silently ignores you.

3. **Cookie auth is fragile.** Unlike API keys, browser cookies expire. If generation fails with auth errors, the user must re-login to Gemini in Chrome.

4. **One server per image is safer.** Reusing a single server process for multiple generations can fail due to session timeouts or rate limits.

5. **Images arrive via file system, not response.** The JSON-RPC response confirms the call succeeded, but the actual PNG appears in `~/Pictures/gemini/` asynchronously. Poll the directory.

6. **`bufsize=0` is critical.** Without unbuffered I/O, JSON-RPC messages get stuck in the buffer and the server appears unresponsive.

7. **Always snapshot before, diff after.** Record existing files in the output directory before each generation call, then find new files by set difference.

---

## OUTPUT DELIVERABLES

After running this skill, the project should contain:

1. **`output/Cover_N_Name.png`** — Generated cover images (1–4 variants)
2. **`output/cover_prompts.json`** — Saved prompts for reproducibility:
```json
[
    {
        "id": 1,
        "name": "Countdown Clock",
        "filename": "Cover_1_Countdown_Clock.png",
        "prompt": "Create a dramatic book cover..."
    }
]
```
3. **User selects final cover** — renamed to `Cover_Final.png`
