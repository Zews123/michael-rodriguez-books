#!/usr/bin/env python3
"""Generate all 4 book cover concepts for 'Shadows of Power' using Gemini API."""

import json
import base64
import urllib.request
import urllib.error
import os
import sys
import time

API_KEY = "AIzaSyBFD0HSvXCHj05oIQedavmpVnwORnPATNc"
OUTPUT_DIR = "/Users/zews/Book/output"

CONCEPTS = {
    1: {
        "name": "The Shadow Network",
        "prompt": (
            "Create a professional book cover image for a nonfiction true crime book. "
            "Portrait orientation, vertical book cover format 2:3 aspect ratio. "
            "Design: Dark navy blue and black background. Manhattan skyline faintly visible in dark blue tones at the bottom. "
            "A solid black silhouette of a man in a business suit standing at the center of the composition. "
            "Thin gold metallic lines radiating outward from the silhouette connecting to small circular nodes, "
            "forming an elegant web-like network pattern - like a conspiracy map. "
            "The silhouette casts an impossibly long dark shadow extending downward. "
            "Title 'SHADOWS OF POWER' in large bold white uppercase sans-serif font prominently at the top. "
            "Subtitle 'Jeffrey Epstein and the Architecture of Impunity' in smaller elegant gold font below the title. "
            "Author name 'MICHAEL RODRIGUEZ' in clean white font at the bottom. "
            "Premium nonfiction aesthetic. Cinematic moody lighting. Minimalist and sophisticated. "
            "Dark, mysterious, powerful mood. No faces, no photographs - purely graphic design."
        ),
    },
    2: {
        "name": "The Island",
        "prompt": (
            "Create a professional book cover image for a nonfiction true crime book. "
            "Portrait orientation, vertical book cover format 2:3 aspect ratio. "
            "Design: Aerial bird's eye view of a small isolated tropical island in a dark, nearly black ocean. "
            "The image is heavily desaturated, almost black and white, with just a subtle hint of dark blue-green for the water. "
            "The island looks small, isolated, and ominous — NOT paradise-like at all. "
            "A single tiny building structure visible on the island. "
            "Dark heavy vignette around edges creating a surveillance-camera or drone footage feel. "
            "Title 'SHADOWS OF POWER' in bold crimson red uppercase font at the top of the cover. "
            "Subtitle 'Jeffrey Epstein and the Architecture of Impunity' in white font below the title. "
            "Author name 'MICHAEL RODRIGUEZ' in white font at the bottom. "
            "Ominous, menacing atmosphere. True crime investigative aesthetic. "
            "Premium nonfiction book cover. Dark and unsettling mood."
        ),
    },
    3: {
        "name": "The Redacted File",
        "prompt": (
            "Create a professional book cover image for a nonfiction true crime book. "
            "Portrait orientation, vertical book cover format 2:3 aspect ratio. "
            "Design: The entire cover looks like an aged, yellowed classified government document or legal filing. "
            "The document has lines of typed text, but most of the text is covered by heavy black redaction bars. "
            "A few fragmentary words are visible through gaps in the redaction: 'trafficking', 'minor', 'immunity', 'classified'. "
            "Title 'SHADOWS OF POWER' appears stamped in bold red ink diagonally or prominently across the document. "
            "A faded 'CONFIDENTIAL' watermark runs diagonally across the page. "
            "Author name 'MICHAEL RODRIGUEZ' appears at the bottom like a signature line on the document. "
            "Subtitle 'Jeffrey Epstein and the Architecture of Impunity' in smaller text. "
            "Realistic paper texture with slight creases and aging. "
            "Investigative journalism aesthetic. Government document feel. Provocative design."
        ),
    },
    4: {
        "name": "Two Faces of Justice",
        "prompt": (
            "Create a professional book cover image for a nonfiction true crime book. "
            "Portrait orientation, vertical book cover format 2:3 aspect ratio. "
            "Design: The image is split vertically down the middle into two contrasting halves. "
            "LEFT half: A grand neoclassical courthouse facade with tall columns and stone steps, "
            "bathed in warm golden light, looking majestic and hopeful — symbolizing the promise of justice. "
            "RIGHT half: The exact same courthouse but in deep shadow, darkness, appearing crumbled, "
            "decayed and broken — symbolizing the failure of justice. "
            "The division line between the two halves is sharp and dramatic. "
            "Title 'SHADOWS OF POWER' spans both halves in large bold white uppercase font with slight shadow. "
            "Subtitle 'Jeffrey Epstein and the Architecture of Impunity' in gold font below the title. "
            "Author name 'MICHAEL RODRIGUEZ' in white font at the bottom. "
            "Powerful visual metaphor. Serious investigative nonfiction aesthetic. Dramatic contrast."
        ),
    },
}


def generate_cover(concept_num: int, concept: dict) -> bool:
    """Generate a single cover concept using Gemini API."""
    name = concept["name"]
    prompt = concept["prompt"]
    print(f"\n{'='*60}")
    print(f"Generating Concept {concept_num}: {name}")
    print(f"{'='*60}")

    # Try different models
    models = [
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash",
    ]

    for model in models:
        print(f"  Trying model: {model}...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseModalities": ["IMAGE", "TEXT"],
            },
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}
        )

        try:
            resp = urllib.request.urlopen(req, timeout=180)
            result = json.loads(resp.read().decode())

            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                for part in parts:
                    if "inlineData" in part:
                        img_b64 = part["inlineData"].get("data", "")
                        mime = part["inlineData"].get("mimeType", "image/png")
                        if img_b64:
                            ext = "png" if "png" in mime else "jpg"
                            out_path = os.path.join(
                                OUTPUT_DIR, f"Cover_Concept{concept_num}_{name.replace(' ', '_')}.{ext}"
                            )
                            with open(out_path, "wb") as f:
                                f.write(base64.b64decode(img_b64))
                            size = os.path.getsize(out_path)
                            print(f"  ✅ SUCCESS! Saved: {out_path}")
                            print(f"     Size: {size:,} bytes")
                            return True
                
                # No image in response
                text_parts = [p.get("text", "") for p in parts if "text" in p]
                if text_parts:
                    print(f"  ⚠️  Model returned text instead of image:")
                    print(f"     {text_parts[0][:200]}...")
            else:
                print(f"  ❌ No candidates in response")
                if "error" in result:
                    print(f"     Error: {result['error'].get('message', '')}")

        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            error_msg = ""
            try:
                error_msg = json.loads(body).get("error", {}).get("message", "")
            except:
                error_msg = body[:200]
            print(f"  ❌ HTTP {e.code}: {error_msg}")

        except urllib.error.URLError as e:
            print(f"  ❌ URL Error: {e.reason}")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # If a specific concept number is provided as argument
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
        if num in CONCEPTS:
            success = generate_cover(num, CONCEPTS[num])
            sys.exit(0 if success else 1)
        else:
            print(f"Unknown concept number: {num}. Valid: 1-4")
            sys.exit(1)

    # Generate all concepts
    results = {}
    for num, concept in CONCEPTS.items():
        success = generate_cover(num, concept)
        results[num] = success
        if num < 4:
            time.sleep(2)  # Brief pause between requests

    print(f"\n{'='*60}")
    print("RESULTS SUMMARY")
    print(f"{'='*60}")
    for num, success in results.items():
        status = "✅ Generated" if success else "❌ Failed"
        print(f"  Concept {num} ({CONCEPTS[num]['name']}): {status}")
    
    generated = sum(1 for s in results.values() if s)
    print(f"\nTotal: {generated}/{len(results)} covers generated")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
