#!/usr/bin/env python3
"""Generate 3 social images for Countdown to Collapse via Gemini MCP."""
import subprocess, json, time, os, glob, shutil

GEMINI_DIR = os.path.expanduser("~/Pictures/gemini")
OUTPUT_DIR = "/Users/zews/Book/Countdown_2040/output/social"
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
    proc = subprocess.Popen(SERVER_CMD,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, bufsize=0)
    try:
        print("  Starting MCP server...")
        time.sleep(15)
        send_msg(proc, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "copilot-cli", "version": "1.0.0"}
        }, msg_id=1)
        send_msg(proc, "notifications/initialized")
        time.sleep(2)
        print(f"  Generating: {prompt[:80]}...")
        send_msg(proc, "tools/call", {
            "name": "gemini_generate_image",
            "arguments": {"prompt": prompt}
        }, msg_id=2)
        elapsed = 0
        while elapsed < timeout:
            current = set(glob.glob(os.path.join(GEMINI_DIR, "*.png")))
            new = current - existing
            if new:
                src = max(new, key=os.path.getmtime)
                shutil.copy2(src, output_path)
                size_kb = os.path.getsize(output_path) / 1024
                print(f"  ✅ Saved: {output_path} ({size_kb:.0f} KB)")
                return True
            time.sleep(5)
            elapsed += 5
        print(f"  ❌ Timeout after {timeout}s")
        return False
    finally:
        proc.terminate()
        try: proc.wait(timeout=5)
        except: proc.kill()

images = [
    {
        "name": "Square (1024x1024)",
        "filename": "countdown_2040_square.png",
        "prompt": "Create a professional book promotional square social media image (1024x1024). Dark cinematic background with deep red and amber tones. In the center, a realistic 3D hardcover book mockup with a dark cover showing a cracked countdown clock in red tones. Below the book mockup, large bold white text 'COUNTDOWN TO COLLAPSE' in clean sans-serif font. Below that in gold/amber text 'The 2040 Crisis'. At the bottom in smaller gold text 'MICHAEL RODRIGUEZ'. Background has subtle smoke and ember particles. Premium nonfiction book promotion design. Professional typography, clean readable text."
    },
    {
        "name": "Banner (1424x752)",
        "filename": "countdown_2040_banner.png",
        "prompt": "Create a professional wide cinematic book promotional banner image (1424x752). Dark background with dramatic red and amber lighting. On the right side, a realistic 3D hardcover book mockup of 'Countdown to Collapse' with dark cover showing cracked clock imagery. On the left side, large bold white text quote 'The clock is ticking. The data doesn't lie.' in elegant serif font. Below the quote, a thin gold horizontal accent line. Below that in bold white text 'COUNTDOWN TO COLLAPSE' and underneath in gold text 'MICHAEL RODRIGUEZ'. Professional book marketing banner design with clean readable typography."
    },
    {
        "name": "Story (768x1376)",
        "filename": "countdown_2040_story.png",
        "prompt": "Create a professional vertical book promotional story image (768x1376). Dark cinematic background with deep crimson and black gradient. At the top, large bold white text with subtle glow effect 'COUNTDOWN TO COLLAPSE' in clean sans-serif font. Below that in gold text 'THE 2040 CRISIS'. In the center, a realistic 3D hardcover book mockup with dark cover showing cracked countdown clock in red tones. Below the book, bold gold text 'AVAILABLE NOW'. At the bottom in white text 'MICHAEL RODRIGUEZ'. Subtle smoke particles and ember effects in background. Premium nonfiction book promotion poster design. Professional clean readable typography."
    }
]

print("=" * 60)
print("SOCIAL IMAGE GENERATION — Countdown to Collapse")
print("=" * 60)

for i, img in enumerate(images, 1):
    print(f"\n[{i}/3] {img['name']}")
    output_path = os.path.join(OUTPUT_DIR, img["filename"])
    success = generate_image(img["prompt"], output_path)
    if not success:
        print("  ⚠️ Failed — will skip")
    if i < len(images):
        print("  Waiting 10s before next...")
        time.sleep(10)

print(f"\n{'=' * 60}")
print("Done! Check output:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    fp = os.path.join(OUTPUT_DIR, f)
    if os.path.isfile(fp):
        print(f"  {f} ({os.path.getsize(fp)/1024:.0f} KB)")
