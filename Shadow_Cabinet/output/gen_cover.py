#!/usr/bin/env python3
"""Generate book covers via Gemini MCP server (one server per image)."""
import subprocess, json, time, os, glob, shutil, sys

GEMINI_DIR = os.path.expanduser("~/Pictures/gemini")
OUTPUT_DIR = "/Users/zews/Book/Shadow_Cabinet/output/"
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
        print("Starting MCP server... (waiting 15s)")
        time.sleep(15)
        
        init = send_msg(proc, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "copilot-cli", "version": "1.0.0"}
        }, msg_id=1)
        print(f"Init: {json.dumps(init, indent=2) if init else 'None'}")
        
        send_msg(proc, "notifications/initialized")
        time.sleep(2)
        
        print(f"Generating image...")
        print(f"Prompt: {prompt[:100]}...")
        resp = send_msg(proc, "tools/call", {
            "name": "gemini_generate_image",
            "arguments": {"prompt": prompt}
        }, msg_id=2)
        print(f"Response: {json.dumps(resp, indent=2) if resp else 'None'}")
        
        elapsed = 0
        while elapsed < timeout:
            current = set(glob.glob(os.path.join(GEMINI_DIR, "*.png")))
            new = current - existing
            if new:
                src = max(new, key=os.path.getmtime)
                shutil.copy2(src, output_path)
                size_mb = os.path.getsize(output_path) / 1024 / 1024
                print(f"Saved: {output_path} ({size_mb:.1f} MB)")
                return output_path
            time.sleep(5)
            elapsed += 5
            if elapsed % 30 == 0:
                print(f"  Waiting... {elapsed}s")
        
        raise TimeoutError(f"No image after {timeout}s")
    
    finally:
        proc.terminate()
        try: proc.wait(timeout=5)
        except: proc.kill()
        print("MCP server stopped.")

covers = {
    1: {
        "filename": "Cover_1_Long_Corridor.png",
        "prompt": "Create a dramatic book cover image for a nonfiction political book called 'The Shadow Cabinet'. A dramatically lit corridor in a neoclassical government building with polished marble floors, tall classical columns, receding into deep shadow with a vanishing point perspective. A single door stands slightly ajar at the far end, emitting a sliver of warm amber light. The corridor is empty. Low directional lighting casts long angular shadows from the columns across the floor. Cinematic, atmospheric, moody. Dark midnight blue and black tones with warm amber accent from the doorway. Slight film grain texture. The space feels occupied as if someone just left. Think David Fincher cinematography meets political thriller. No text on the image. Aspect ratio: portrait (2:3), suitable for book cover."
    },
    2: {
        "filename": "Cover_2_Redacted_File.png",
        "prompt": "Create a minimalist book cover image for a nonfiction investigative book about secret government programs. A close-up photograph of a declassified government document on aged cream-colored paper. Several lines of typewritten text are visible but key words and phrases are covered by thick black redaction bars made with a heavy black marker. A faint CLASSIFIED stamp in washed-out red ink appears at an angle in the upper corner. The document shows official letterhead or a government seal watermark. The paper has slight aging, foxing, and fold marks. Photorealistic, documentary style. The feeling of evidence, something that was never meant to be seen. Overhead lighting, shot from above as if photographing documents on a desk. No text on the image except the redaction bars and stamp. Aspect ratio: portrait (2:3), suitable for book cover."
    },
    3: {
        "filename": "Cover_3_Architecture_of_Power.png",
        "prompt": "Create a dramatic book cover image for a book about hidden power structures and conspiracy. A moody aerial nighttime photograph of a grand government building or capitol dome seen from above, with a geometric network of glowing connection lines overlaid like a data visualization or constellation map connecting different points of power. The lines glow in subtle gold and blue against the dark city below. The feeling is surveillance, watching from above, mapping invisible connections. Deep dark blue and black atmosphere with gold accent lines. Cinematic, modern, slightly dystopian. Think satellite imagery meets data visualization meets political thriller. No text on the image. Aspect ratio: portrait (2:3), suitable for book cover."
    },
    4: {
        "filename": "Cover_4_Power_Structure.png",
        "prompt": "Create a striking book cover image for a political nonfiction book about shadowy power organizations. A dramatic photograph of a large round conference table in a dark, wood-paneled boardroom, shot from directly above. The table is empty except for leather portfolios at each seat. The chairs are pulled out as if the meeting just ended. A single overhead light illuminates the table creating a pool of warm light surrounded by darkness. The wood paneling and carpet disappear into shadow. The composition creates a sense of absence, powerful people were just here, making decisions that affect millions. No people visible. Dark, atmospheric, tension. Warm wood tones against deep shadow. No text on the image. Aspect ratio: portrait (2:3), suitable for book cover."
    }
}

if __name__ == "__main__":
    cover_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cover = covers[cover_num]
    output_path = os.path.join(OUTPUT_DIR, cover["filename"])
    print(f"\n{'='*60}")
    print(f"Generating Cover {cover_num}: {cover['filename']}")
    print(f"{'='*60}\n")
    generate_image(cover["prompt"], output_path)
