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
    
    proc = subprocess.Popen(SERVER_CMD,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, bufsize=0)
    
    try:
        print("Starting MCP server...")
        time.sleep(15)
        
        resp = send_msg(proc, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "copilot-cli", "version": "1.0.0"}
        }, msg_id=1)
        print(f"Init: {'OK' if resp else 'FAILED'}")
        
        send_msg(proc, "notifications/initialized")
        time.sleep(2)
        
        print(f"Generating: {prompt[:80]}...")
        resp2 = send_msg(proc, "tools/call", {
            "name": "gemini_generate_image",
            "arguments": {"prompt": prompt}
        }, msg_id=2)
        print(f"Tool response: {'OK' if resp2 else 'FAILED'}")
        
        elapsed = 0
        while elapsed < timeout:
            current = set(glob.glob(os.path.join(GEMINI_DIR, "*.png")))
            new = current - existing
            if new:
                src = max(new, key=os.path.getmtime)
                shutil.copy2(src, output_path)
                size_kb = os.path.getsize(output_path) / 1024
                print(f"Saved: {output_path} ({size_kb:.0f} KB)")
                return True
            time.sleep(5)
            elapsed += 5
        
        print(f"Timeout after {timeout}s")
        # Check stderr for errors
        stderr = proc.stderr.read() if proc.stderr else ""
        if stderr:
            print(f"Server stderr: {stderr[:500]}")
        return False
    
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    finally:
        proc.terminate()
        try: proc.wait(timeout=5)
        except subprocess.TimeoutExpired: os.system(f"kill -9 {proc.pid}")

covers = [
    {
        "prompt": "Create a dramatic book cover design. Two silk ribbons — one with the American stars and stripes pattern, one with the Iranian green-white-red pattern — tied together in a complex, fraying knot against a pure charcoal black background. The knot is tight and strained, with loose threads unraveling from both ribbons. Dramatic side lighting creates sharp shadows. Moody, tense atmosphere. Photorealistic fabric texture. No text on the image. Aspect ratio: portrait (2:3), suitable for book cover.",
        "filename": "Cover_1_Knotted_Flags.png"
    },
    {
        "prompt": "Create a powerful book cover design. A dramatic black and white archival-style photograph showing a crowd of people in front of a burning building, reminiscent of 1979 Tehran. Over the photograph, a gradient wash of blood red bleeds from the top. At the bottom, a thin strip of modern color — a contemporary city skyline. The contrast between old and new, chaos and order. Gritty, documentary atmosphere. No text on the image. Aspect ratio: portrait (2:3), suitable for book cover.",
        "filename": "Cover_2_Documentary.png"
    },
    {
        "prompt": "Create a striking minimalist book cover design. A deep navy blue background. In the center, the outline of Iran's geographic shape formed by a jagged, glowing crack — like shattered glass or fractured earth. Through the crack, warm amber-gold light spills out, suggesting fire or desert sun. The crack extends beyond Iran's borders. Clean, modern, geometric. Dark and sophisticated atmosphere. No text on the image. Aspect ratio: portrait (2:3), suitable for book cover.",
        "filename": "Cover_3_Cracked_Map.png"
    },
    {
        "prompt": "Create a dramatic split book cover design. The image is divided vertically down the center. Left half: the dome of the US Capitol Building in cool steel-blue tones, with an American flag waving. Right half: the Azadi Tower in Tehran in warm amber-gold tones, with an Iranian flag waving. Where the two halves meet in the center, the images fracture and blend into each other like broken mirror pieces. Dramatic lighting from both sides. Cinematic, tense atmosphere. No text on the image. Aspect ratio: portrait (2:3), suitable for book cover.",
        "filename": "Cover_4_Two_Capitals.png"
    }
]

output_dir = "/Users/zews/Book/Persian_Grudge/output/"
results = []

for i, cover in enumerate(covers, 1):
    print(f"\n{'='*50}")
    print(f"Cover {i}/{len(covers)}: {cover['filename']}")
    print(f"{'='*50}")
    
    output_path = os.path.join(output_dir, cover["filename"])
    success = generate_image(cover["prompt"], output_path)
    results.append((cover["filename"], success))
    
    if i < len(covers):
        print("Waiting 10s...")
        time.sleep(10)

print(f"\n{'='*50}")
print("RESULTS:")
for name, ok in results:
    print(f"  {'OK' if ok else 'FAIL'} {name}")
print(f"{'='*50}")

with open(os.path.join(output_dir, "cover_prompts.json"), "w") as f:
    json.dump(covers, f, indent=2)
print("Prompts saved to cover_prompts.json")
