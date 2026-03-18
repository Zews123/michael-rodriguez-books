#!/usr/bin/env python3
"""
Generate professional book covers via Gemini MCP - WITH text embedded.
Book: "The Shadow Cabinet" by Michael Rodriguez
Usage: python3 gen_cover_v2.py [1|2|3|4|all]
"""
import subprocess, json, time, os, glob, shutil, sys

GEMINI_DIR = os.path.expanduser("~/Pictures/gemini")
OUTPUT_DIR = "/Users/zews/Book/Shadow_Cabinet/output/"
SERVER_CMD = [
    "uv", "run", "--python", "3.12",
    "--with", "gemini-webapi-mcp[watermark] @ git+https://github.com/AndyShaman/gemini-webapi-mcp.git",
    "gemini-webapi-mcp"
]

COVERS = {
    1: {
        "filename": "Cover_1_Corridor_v2.png",
        "prompt": (
            "Professional nonfiction book cover design, 2:3 portrait ratio (6x9 inches). "
            "VISUAL: A dramatically lit corridor in a neoclassical government building, "
            "marble floors, tall stone columns receding into deep shadow. At the far end, "
            "a single door stands slightly ajar emitting warm amber light. Low directional "
            "lighting casts long angular shadows from columns across the polished floor. "
            "Cinematic, atmospheric, slightly aged look with subtle film grain. No people. "
            "TYPOGRAPHY: Bottom 40% has dark semi-transparent gradient overlay fading to near-black. "
            "Centered large antique gold elegant Roman serif all-caps text: 'THE SHADOW' on one line "
            "then 'CABINET' on next line. A thin gold horizontal rule with small diamond below. "
            "Centered smaller silver-grey italic serif: 'Conspiracy, Power, and the Architecture of Hidden Control'. "
            "At very bottom centered small white spaced caps: 'MICHAEL RODRIGUEZ'. "
            "All text crisp, professional, correctly spelled. Style: Penguin Press political nonfiction."
        )
    },
    2: {
        "filename": "Cover_2_Redacted_v2.png",
        "prompt": (
            "Professional nonfiction book cover design, 2:3 portrait ratio (6x9 inches). "
            "VISUAL: Aged parchment off-white background with faint barely-visible horizontal "
            "ruled lines, very light grey watermark circular generic government-style seal "
            "(not a real seal), faint washed-out red CLASSIFIED stamp angled 15 degrees in upper right. "
            "TYPOGRAPHY centered on cover: Small tracked dark grey elegant serif 'THE'. "
            "Below it: very large bold serif 'SHADOW' with a solid black imperfect hand-drawn "
            "redaction bar covering the word (text still faintly visible under bar, as if censored). "
            "Below that: very large bold serif 'CABINET' clean and unobscured. "
            "Below that in Courier typewriter monospace smaller: "
            "'Conspiracy, Power, and the Architecture of Hidden Control_' with trailing underscore cursor. "
            "At bottom: 'MICHAEL RODRIGUEZ' in clean serif spaced caps. "
            "Generous white space. Intellectual restraint. Serious investigative journalism aesthetic. "
            "Like a real declassified government document."
        )
    },
    3: {
        "filename": "Cover_3_Architecture_v2.png",
        "prompt": (
            "Professional nonfiction book cover design, 2:3 portrait ratio (6x9 inches). "
            "VISUAL: Upper 55% is a black and white photojournalistic photo of a massive neoclassical "
            "government building, low angle looking up at enormous stone columns, high contrast "
            "documentary grain, sky dissolves to near-white at top, deep blue-black shadows. "
            "A single thin red diagonal line overlaid as the ONLY color element. "
            "Lower 45% is a solid pure black band, hard editorial cut no gradient. "
            "TYPOGRAPHY on black band, left-aligned throughout: "
            "Small white tracked modern bold sans-serif 'MICHAEL RODRIGUEZ'. "
            "Then very large bold white modern sans-serif 'THE SHADOW' on one line, 'CABINET' on next. "
            "Then smaller silver-grey light weight sans-serif "
            "'Conspiracy, Power, and the Architecture of Hidden Control'. "
            "All text left-aligned. Editorial design style matching serious investigative journalism."
        )
    },
    4: {
        "filename": "Cover_4_Network_v2.png",
        "prompt": (
            "Professional nonfiction book cover design, 2:3 portrait ratio (6x9 inches). "
            "VISUAL: Pure black background. Behind everything: enormous barely-visible dark charcoal "
            "oversized text 'SHADOW' bleeding off all edges as subliminal hidden layer. "
            "Over this: network of thin teal-green lines connecting small circular nodes scattered "
            "organically across cover suggesting conspiracy organizational chart. "
            "TYPOGRAPHY visible foreground text: "
            "At top of cover: 'MICHAEL RODRIGUEZ' in off-white spaced bold geometric sans-serif. "
            "In lower third: 'THE' in off-white bold geometric sans-serif, "
            "'SHADOW' in bright teal bold geometric sans-serif as highlighted accent color, "
            "'CABINET' in off-white bold geometric sans-serif. "
            "Below title: 'Conspiracy, Power, and the Architecture of Hidden Control' "
            "in muted teal-green lighter weight sans-serif. "
            "Contemporary bold design. Modern political nonfiction. "
            "The word SHADOW appears both hidden large in background and visible small in foreground."
        )
    }
}


def send_msg(proc, method, params=None, msg_id=None):
    msg = {"jsonrpc": "2.0", "method": method}
    if params:
        msg["params"] = params
    if msg_id is not None:
        msg["id"] = msg_id
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
    if msg_id is not None:
        line = proc.stdout.readline()
        return json.loads(line) if line else None


def generate_cover(cover_num, timeout=180):
    cover = COVERS[cover_num]
    output_path = os.path.join(OUTPUT_DIR, cover["filename"])
    os.makedirs(GEMINI_DIR, exist_ok=True)
    existing = set(glob.glob(os.path.join(GEMINI_DIR, "*.png")))

    print(f"\n{'='*60}")
    print(f"Cover {cover_num}: {cover['filename']}")
    print(f"{'='*60}")

    proc = subprocess.Popen(
        SERVER_CMD,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, bufsize=0
    )

    try:
        print("Starting MCP server (waiting 15s)...")
        time.sleep(15)

        send_msg(proc, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "copilot-cli", "version": "1.0.0"}
        }, msg_id=1)
        send_msg(proc, "notifications/initialized")
        time.sleep(2)

        print("Sending prompt to Gemini...")
        send_msg(proc, "tools/call", {
            "name": "gemini_generate_image",
            "arguments": {"prompt": cover["prompt"]}
        }, msg_id=2)

        print("Waiting for image...")
        elapsed = 0
        while elapsed < timeout:
            current = set(glob.glob(os.path.join(GEMINI_DIR, "*.png")))
            new = current - existing
            if new:
                src = max(new, key=os.path.getmtime)
                shutil.copy2(src, output_path)
                size_mb = os.path.getsize(output_path) / 1024 / 1024
                print(f"SUCCESS: {output_path} ({size_mb:.1f} MB)")
                return output_path
            time.sleep(5)
            elapsed += 5
            if elapsed % 30 == 0:
                print(f"  Still waiting... ({elapsed}s elapsed)")

        print(f"TIMEOUT after {timeout}s")
        return None

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            import signal
            os.kill(proc.pid, signal.SIGKILL)
        print("MCP server stopped.")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    nums = [1, 2, 3, 4] if arg == "all" else [int(arg)]

    results = []
    for i, num in enumerate(nums):
        result = generate_cover(num)
        results.append((num, result))
        if i < len(nums) - 1:
            print("Waiting 10s before next cover...")
            time.sleep(10)

    print("\nSUMMARY:")
    for num, path in results:
        status = "OK" if path else "FAIL"
        print(f"  Cover {num}: {status} - {path or 'FAILED'}")
