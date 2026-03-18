# SOCIAL MEDIA PROMOTION — Agent Prompt

## LAUNCH INSTRUCTION

User provides only:
- Book folder path (e.g. `/Users/zews/Book/Writers_Agent/Shadows_of_Power/`)
- Book page URL on the site (e.g. `https://michaelrodriguezbooks.com/books/{{book-slug}}/`)
- Amazon direct link (e.g. `https://www.amazon.com/dp/B0GNZ42KLK`)
- Free Chapter page URL (e.g. `https://michaelrodriguezbooks.com/books/free-chapter-{{book-slug}}/`)

Everything else — extract automatically from existing files.

---

## LINK STRATEGY — DUAL LINKS (Amazon + Free Chapter)

Every book has **two key links** for social media promotion:
1. **Amazon direct link** — for immediate sales (`https://www.amazon.com/dp/{{ASIN}}`)
2. **Free Chapter link** — landing page with free chapters + Kit email form for lead generation

### Platform link rules:

| Platform | Links to include |
|----------|-----------------|
| **Medium** | BOTH — Amazon + Free Chapter (in CTA section) |
| **Blogspot** | BOTH — Amazon + Free Chapter (in CTA section) |
| **LinkedIn** | BOTH — Amazon + Free Chapter |
| **Facebook** | BOTH — Amazon + Free Chapter |
| **Telegram** | BOTH — Amazon + Free Chapter |
| **X / Twitter** | Amazon link ONLY (space limited, 280 chars) |
| **Instagram** | "Link in bio →" (no direct links) |
| **Pinterest** | NO link (user adds separately) |

> ⚠️ On platforms with enough space, ALWAYS include both: "📦 Get it on Amazon: [link]" and "📖 Read free chapters: [link]". The Free Chapter link captures emails via Kit form, which is more valuable long-term than a single sale.

---

## STAGE 0 — EXTRACT ALL DATA

Read from the book folder:

### From `output/Final_Book.docx` — extract:
- Book title and subtitle
- Core themes, key revelations, author's tone and style
- Most provocative facts and statistics from the book
- Chapter structure

### From `output/Publishing_Package.txt` — extract:
- Long SEO description
- Short description (tagline)
- Keywords list
- Author bio
- All store links (Amazon, Apple, Kobo, B&N)

### Cover image:
- Find `assets/images/{{Book_Slug}}.webp` in the GitHub repo
- **Analyze the cover carefully** — extract dominant colors, visual elements, and mood
- Use these details in image generation prompts: `[COVER_VISUAL_DESCRIPTION]`, `[BOOK_THEME_COLORS]`
- Example: cover shows a cracked clock → prompt includes "cracked countdown clock in red tones"

### Hook quote for banner:
- Extract the most provocative 1-2 sentence quote from the book (for banner left-side text)
- Must be impactful and readable in large font at banner scale

> Report extracted data summary before proceeding.

---

## STAGE 1 — GENERATE SOCIAL IMAGES (via Gemini MCP)

Generate **3 marketing images** using `gemini_generate_image` via Gemini MCP server.

> ⚠️ **CRITICAL RULES:**
> 1. **NEVER** include "No text on the image" in prompts — this produces raw background images without marketing value
> 2. **ALWAYS** request a "realistic 3D hardcover book mockup" — this is the key visual element
> 3. **ALWAYS** specify exact text to render: title, subtitle, author name, CTA
> 4. **ALWAYS** specify typography details: font style, color, size, positioning
> 5. End every prompt with "Professional clean readable typography"
> 6. Specify exact pixel dimensions in the prompt

### Gemini MCP Technical Setup

```python
# Server command — start fresh process for EACH image
SERVER_CMD = [
    "uv", "run", "--python", "3.12",
    "--with", "gemini-webapi-mcp[watermark] @ git+https://github.com/AndyShaman/gemini-webapi-mcp.git",
    "gemini-webapi-mcp"
]
# MCP config reference: /Users/zews/Book/.vscode/mcp.json
# Output directory: ~/Pictures/gemini/ (poll for new .png files)
```

> ⚠️ **CRITICAL — MCP TRANSPORT PROTOCOL:**
>
> This server uses **raw JSON Lines** (newline-delimited JSON), **NOT** the standard
> `Content-Length` HTTP-style framing. This is the #1 reason Gemini MCP fails.
>
> ❌ **WRONG** (will cause "Invalid JSON" errors):
> ```
> Content-Length: 166\r\n\r\n{"jsonrpc":"2.0","id":1,...}
> ```
>
> ✅ **CORRECT** (raw JSON line terminated with `\n`):
> ```
> {"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}\n
> ```
>
> If you see `"Invalid JSON: expected value at line 1 column 1"` in stderr —
> you are using Content-Length framing. Switch to raw JSON lines immediately.

### Gemini MCP — Complete Working Protocol (proven March 2026)

The following Python script is the **reference implementation** that reliably generates
all 3 images. Use this exact protocol — do NOT improvise alternatives.

```python
import subprocess, time, os, select, json, glob, shutil

GEMINI_DIR = os.path.expanduser("~/Pictures/gemini/")

def get_files():
    return set(glob.glob(os.path.join(GEMINI_DIR, "*.png")))

def send(proc, data):
    """Send JSON-RPC message as raw JSON line (NOT Content-Length framing!)"""
    line = json.dumps(data) + "\n"
    proc.stdin.write(line.encode("utf-8"))
    proc.stdin.flush()

def recv(proc, timeout=300):
    """Read JSON-RPC response. Timeout must be ≥300s for image generation."""
    buf = b""
    start = time.time()
    while time.time() - start < timeout:
        r, _, _ = select.select([proc.stdout], [], [], 1.0)
        if r:
            chunk = os.read(proc.stdout.fileno(), 65536)
            if chunk:
                buf += chunk
                text = buf.decode("utf-8", errors="replace")
                for line in text.strip().split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        if "id" in obj and ("result" in obj or "error" in obj):
                            return obj
                    except:
                        pass
    return None

def drain_stderr(proc):
    """Drain stderr to prevent buffer blocking."""
    while True:
        r, _, _ = select.select([proc.stderr], [], [], 0.1)
        if r:
            os.read(proc.stderr.fileno(), 65536)
        else:
            break

def start_server():
    """Start fresh MCP server. Returns subprocess or None."""
    cmd = ["uv", "run", "--python", "3.12",
           "--with", "gemini-webapi-mcp[watermark] @ git+https://github.com/AndyShaman/gemini-webapi-mcp.git",
           "gemini-webapi-mcp"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, bufsize=0)
    time.sleep(15)  # Wait for Gemini client to init with Chrome cookies
    drain_stderr(proc)

    # Step 1: initialize (raw JSON line!)
    send(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "book-factory", "version": "1.0"}
    }})
    resp = recv(proc, timeout=15)
    if not (resp and "result" in resp):
        proc.terminate()
        return None

    # Step 2: send initialized notification
    send(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})
    time.sleep(2)
    drain_stderr(proc)
    return proc

def generate_image(proc, prompt, output_name, output_dir, req_id=3):
    """Generate one image. Returns True/False."""
    existing = get_files()
    send(proc, {"jsonrpc": "2.0", "id": req_id, "method": "tools/call", "params": {
        "name": "gemini_generate_image",
        "arguments": {"prompt": prompt}
    }})
    # Wait for JSON-RPC response (up to 5 minutes)
    resp = recv(proc, timeout=300)
    drain_stderr(proc)
    # Also poll filesystem — images may appear before/after response
    new_file = None
    for i in range(60):
        time.sleep(5)
        current = get_files()
        new_files = current - existing
        if new_files:
            new_file = max(new_files)
            break
    if new_file:
        dest = os.path.join(output_dir, output_name + ".png")
        shutil.copy2(new_file, dest)
        return True
    return False
```

**Key technical notes:**
- Start a **fresh MCP server process** for each image (reusing sessions can fail)
- Wait **15s** after server start before `initialize` (Gemini client inits Chrome cookies)
- Transport: **raw JSON lines** (`{json}\n`) — NOT `Content-Length` framing
- Image generation takes **30s–180s** — set timeout to **300s minimum**
- Images appear in `~/Pictures/gemini/` as `YYYYMMDDHHMMSS_0.png` — poll every 5s
- After response, also poll filesystem — sometimes files appear with delay
- Wait **15s** between separate image generations to avoid rate limiting
- **DO NOT fall back to Pillow** — Gemini MCP works reliably with this protocol

### Prompt Templates (proven successful)

#### Image 1 — Square post (1024×1024px)
For: Instagram, Facebook, Telegram
```
Create a professional book promotional square social media image (1024x1024).
Dark cinematic background with [BOOK_THEME_COLORS — e.g. deep red and amber] tones.
In the center, a realistic 3D hardcover book mockup with a dark cover showing
[COVER_VISUAL_DESCRIPTION — e.g. a cracked countdown clock in red tones].
Below the book mockup, large bold white text '[BOOK_TITLE]' in clean sans-serif font.
Below that in gold/amber text '[SUBTITLE]'.
At the bottom in smaller gold text '[AUTHOR_NAME]'.
Background has subtle smoke and ember particles.
Premium nonfiction book promotion design.
Professional clean readable typography.
```

#### Image 2 — Landscape banner (1424×752px)
For: LinkedIn, Facebook link preview, Medium header
```
Create a professional wide cinematic book promotional banner image (1424x752).
Dark background with dramatic [THEME_COLORS] lighting.
On the right side, a realistic 3D hardcover book mockup of '[BOOK_TITLE]'
with dark cover showing [COVER_VISUAL_DESCRIPTION].
On the left side, large bold white text quote '[HOOK_QUOTE — e.g. The clock is ticking. The data doesn't lie.]'
in elegant serif font.
Below the quote, a thin gold horizontal accent line.
Below that in bold white text '[BOOK_TITLE]'
and underneath in gold text '[AUTHOR_NAME]'.
Professional book marketing banner design with clean readable typography.
```

#### Image 3 — Vertical story (768×1376px)
For: Instagram Stories, Pinterest
```
Create a professional vertical book promotional story image (768x1376).
Dark cinematic background with [THEME_COLORS — e.g. deep crimson and black] gradient.
At the top, large bold white text with subtle glow effect '[BOOK_TITLE]'
in clean sans-serif font.
Below that in gold text '[SUBTITLE]'.
In the center, a realistic 3D hardcover book mockup with dark cover showing
[COVER_VISUAL_DESCRIPTION].
Below the book, bold gold text 'AVAILABLE NOW'.
At the bottom in white text '[AUTHOR_NAME]'.
Subtle smoke particles and ember effects in background.
Premium nonfiction book promotion poster design.
Professional clean readable typography.
```

### Save images to:
```
{{Book_Folder}}/output/social/{{Book_Slug}}_square.png
{{Book_Folder}}/output/social/{{Book_Slug}}_banner.png  
{{Book_Folder}}/output/social/{{Book_Slug}}_story.png
```

### 🔄 Pillow Fallback — LAST RESORT ONLY

> ⚠️ **DO NOT use Pillow as the first approach.** Gemini MCP produces dramatically better
> marketing images (3D book mockups, cinematic lighting, professional composition).
> Pillow fallback produces flat, template-like images that users will reject.
>
> **Use Pillow ONLY if:**
> 1. You verified Gemini MCP is completely unavailable (server won't start at all)
> 2. You tried the raw JSON line protocol (not Content-Length framing)
> 3. You waited the full 300s timeout per image
> 4. You tried at least 2 separate server restarts
>
> If Gemini times out, the most common cause is **wrong transport protocol**
> (Content-Length instead of raw JSON lines). Fix that first before falling back.

If Gemini MCP is truly unavailable after all the above checks, create a marketing image using Python Pillow with text overlay on a Gemini-generated background:

**Step 1:** Generate a plain background via Gemini (simpler prompts are less likely to fail):
```
Dark cinematic vertical background (768x1376) with [THEME_COLORS] gradient.
Moody atmospheric smoke and particle effects. No text, no objects — just background.
```

**Step 2:** Apply text overlay with Pillow:

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.open("background.png").convert("RGBA")
draw = ImageDraw.Draw(img)

# === Gradient darkening for text readability ===
# Top gradient: 300px from top, opacity 180→0
for y in range(300):
    alpha = int(180 * (1 - y / 300))
    draw.rectangle([(0, y), (img.width, y + 1)], fill=(0, 0, 0, alpha))

# Bottom gradient: 400px from bottom, opacity 0→200
bh = 400
for y in range(bh):
    alpha = int(200 * (y / bh))
    draw.rectangle([(0, img.height - bh + y), (img.width, img.height - bh + y + 1)],
                   fill=(0, 0, 0, alpha))

# === Fonts (macOS paths) ===
font_title = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 52, index=11)   # Bold
font_sub   = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 28, index=6)    # DemiBold
font_cta   = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 36, index=11)   # Bold
font_author= ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 22, index=6)    # DemiBold

# === Glow effect for title ===
glow_offsets = [(-2,-2),(-2,2),(2,-2),(2,2),(-3,0),(3,0),(0,-3),(0,3)]
for dx, dy in glow_offsets:
    draw.text((x + dx, y + dy), title_text, font=font_title, fill=(180, 0, 0, 100), anchor="mt")
draw.text((x, y), title_text, font=font_title, fill="white", anchor="mt")

# === Colors ===
WHITE = (255, 255, 255)
GOLD  = (255, 200, 50)        # Bright gold for CTA
GOLD2 = (218, 165, 32)        # Classic gold for subtitle

# === Letter-spacing for author name ===
spaced = "  ".join(list("AUTHOR NAME"))  # "A  U  T  H  O  R  ..."
draw.text((cx, y), spaced, font=font_author, fill=GOLD, anchor="mt")

img = img.convert("RGB")
img.save("output_story.png", quality=95)
```

**Key Pillow techniques:**
- Always use RGBA mode for transparency compositing
- Gradient darkening at top and bottom ensures text readability on any background
- Glow effect: draw text at 8 offsets with semi-transparent color, then white on top
- Letter-spacing via spaced characters for elegant author name
- Available macOS fonts: `Avenir Next.ttc`, `HelveticaNeue.ttc`, `ArialHB.ttc`
- Font index matters: check with `ImageFont.truetype(path, size, index=N)`

> ⚠️ **Remember:** Pillow is a degraded fallback. Always prefer Gemini MCP — it produces
> 3D book mockups and cinematic compositions that Pillow cannot replicate.

---

## STAGE 2 — WRITE ALL POSTS

Write posts for all 8 platforms. **ALL posts in English** (including Telegram), for English-speaking audience.
Communicate with user in **Russian**.

Use Herman Hook method in every post:
- Unexpected fact or statistic from the book
- Emotional trigger or provocative question
- Immediate reader relevance

Style: author's voice — narrative-driven, investigative, slight irony, energetic.
No generic "buy this book" language. Every post must feel organic.

---

### 📝 POST 1 — MEDIUM (long-form SEO article)

**Format:** Full article, 800–1200 words
**SEO title:** max 55 characters, keyword-rich
**Structure:**
1. Herman Hook opening (unexpected fact, provocative question)
2. Section 1: Core problem the book addresses (300 words)
3. Section 2: Key revelations — what readers will discover (300 words)  
4. Section 3: Why this book, why now (200 words)
5. CTA: dual links — Amazon direct purchase + Free Chapter page (2–3 times throughout)
6. Closing: share appeal

**SEO requirements:**
- Primary keyword in title, first paragraph, one subheading
- Secondary keywords naturally distributed
- Meta description suggestion (155 chars)

**Also provide 5 Medium Topics tags:**
```
Topics: [tag1], [tag2], [tag3], [tag4], [tag5]
```

> ⚠️ **MEDIUM FORMAT RULES — CRITICAL:**
> Use standard Markdown. Medium does NOT parse Markdown on copy-paste.
> User opens the .md file in VS Code → `Cmd+Shift+V` (Markdown Preview) → copies rendered text → pastes into Medium.
> - Headings: `# H1` for title, `## H2` for sections
> - Bold: `**text**`
> - Italic: `*text*`
> - Bullet lists: `- item`
> - Numbered lists: `1. item`
> - Links: `[link text](url)`
> - Horizontal divider: `---`
> - Paragraphs: separated by blank lines
> Do NOT use `[H2:]`, `[BOLD:]`, `[ITALIC:]` markers — they appear as literal text.
>
> **OUTPUT:** Save as separate file `{{Book_Folder}}/output/social/medium_article_{{slug}}.md`
> (only the article body — no SEO metadata, no `## MEDIUM` header)

---

### 📝 POST 2 — BLOGSPOT / BLOGGER (SEO article with image)

**Format:** Blog post, 600–900 words
**Structure:** same as Medium but slightly shorter

> ⚠️ **BLOGSPOT FORMAT RULES — CRITICAL:**
> Output in **pure HTML only**. Never use Markdown syntax.
> Blogspot uses an HTML editor — Markdown symbols appear as raw text.
> - Headings: `<h2>`, `<h3>` tags — NOT `###` or `####`
> - Bold: `<strong>text</strong>` — NOT `**text**`
> - Italic: `<em>text</em>` — NOT `*text*`
> - Bullet lists: `<ul><li>item</li></ul>` — NOT `- item`
> - Numbered lists: `<ol><li>item</li></ol>`
> - Paragraphs: wrap in `<p>text</p>` tags
> - Links: `<a href="url">link text</a>`
> - Line breaks: `<br>` if needed

**Must include at the very top:**
```html
<img src="https://michaelrodriguezbooks.com/assets/images/{{Book_Slug}}.webp" 
     alt="{{BOOK_TITLE}} by Michael Rodriguez"
     style="width:100%; max-width:600px; height:auto;">
```
- Internal anchor links to book page AND Free Chapter page using `<a href="...">` tags
- Meta description suggestion (155 chars)

---

### 📝 POST 3 — LINKEDIN (professional article)

**Format:** 600–900 words, structured by blocks
**Title:** max 55 characters
**Tone:** professional analyst, thought leader
**Structure:**
1. Hook — data point or contrarian insight
2. The problem / context (business/economic angle)
3. What the research reveals (3 key points, each with brief explanation)
4. Author credibility paragraph
5. CTA — Amazon direct link + Free Chapter link, invite discussion with question

**End with discussion question:**
```
What do you think about [core theme]? Share in comments ↓
```

> ⚠️ **LINKEDIN FORMAT RULES — CRITICAL:**
> Use standard Markdown — same as Medium.
> User opens the .md file in VS Code → `Cmd+Shift+V` (Markdown Preview) → copies rendered text → pastes into LinkedIn.
> - Headings: `# H1` for title, `### H3` for sections
> - Bold: `**text**`
> - Italic: `*text*`
> - Links: `[link text](url)`
> - Paragraphs: separated by blank lines
> Do NOT use `[H2:]`, `[BOLD:]`, `[ITALIC:]` markers — they appear as literal text.
>
> **OUTPUT:** Save as separate file `{{Book_Folder}}/output/social/linkedin_article_{{slug}}.md`
> (only the article body — no metadata, no `## LINKEDIN` header)

---

### 📝 POST 4 — X / TWITTER (thread)

**Format:** Thread of 4 tweets
**Each tweet:** max 280 characters
**Tweet 1:** Herman Hook — shocking fact or stat (no link)
**Tweet 2:** Key revelation from book
**Tweet 3:** "What you'll discover in [Book Title]:" + 3 bullet points
**Tweet 4:** CTA + Amazon direct link (no Free Chapter — not enough space)

Also provide **single standalone tweet** (max 280 chars) for one-off posting.

---

### 📝 POST 5 — FACEBOOK (engaging post)

**Format:** 150–300 words
**Tone:** conversational but intelligent
**Structure:**
1. Hook question or bold statement (1–2 sentences)
2. Core narrative — pull from book's most surprising insight
3. "Here's what the book reveals:" + 3 short bullets
4. CTA with dual links: Amazon + Free Chapter
5. End with question to drive comments

---

### 📝 POST 6 — PINTEREST (visual description)

**Format:** 100–150 words, NO link (user adds separately)
**Tone:** discovery, curiosity, value
**Structure:**
1. Bold opening statement
2. "In this book you'll discover:" + 4–5 bullets
3. Author name and book title at end
**Note:** optimized for Pinterest search — use descriptive, keyword-rich language

---

### 📝 POST 7 — INSTAGRAM (caption)

**Format:** 150–220 words + hashtags
**Structure:**
1. Hook — first line must stop the scroll (bold claim or question)
2. 3–4 short punchy paragraphs (single sentences work well)
3. CTA: "Link in bio →"
4. Line break, then 20–25 hashtags in first comment style:

```
#[keyword] #[keyword] #nonfiction #investigativejournalism 
#[booktopic] #mustread #newbook #bookstagram #bookrecommendations
[+15 more relevant]
```

---

### 📝 POST 8 — TELEGRAM (with link)

**Format:** 120–180 words **in English** (NOT Russian)
**Tone:** direct, punchy, slightly informal
**Structure:**
1. Emoji opener + bold hook
2. 3 bullet points — key things readers will learn
3. "Available now:" + Amazon direct link + Free Chapter link + store links (Apple)
4. 3–5 relevant hashtags

---

## STAGE 3 — OUTPUT PACKAGE

Save all posts to: `{{Book_Folder}}/output/social/Social_Package.md`

Format:
```markdown
# SOCIAL MEDIA PACKAGE — {{BOOK_TITLE}}
Generated: {{DATE}}

---
## IMAGES GENERATED
- Square (Instagram/FB/TG): {{Book_Folder}}/output/social/{{slug}}_square.png
- Banner (LinkedIn/Medium): {{Book_Folder}}/output/social/{{slug}}_banner.png
- Story (Stories/Pinterest): {{Book_Folder}}/output/social/{{slug}}_story.png

---
## MEDIUM
[full article]

---
## BLOGSPOT
[full article with HTML image]

---
## LINKEDIN
[article]

---
## X / TWITTER
### Thread:
[4 tweets numbered]

### Standalone tweet:
[single tweet]

---
## FACEBOOK
[post]

---
## PINTEREST
[description]

---
## INSTAGRAM
### Caption:
[caption]

### Hashtags (post as first comment):
[hashtags]

---
## TELEGRAM
[post with link]
```

---

## PUBLICATION CHECKLIST

Before delivering to user, verify:

- [ ] All posts written in English (including Telegram — NO Russian)
- [ ] Herman Hook present in every post
- [ ] **Dual links** (Amazon + Free Chapter) included in: Medium, Blogspot, LinkedIn, Facebook, Telegram
- [ ] **Amazon-only link** in Twitter (space limited)
- [ ] Pinterest post has NO link (user adds manually)
- [ ] Instagram ends with "Link in bio →"
- [ ] All 3 social images generated and saved
- [ ] Images contain: 3D book mockup + title + author + CTA text (NOT raw backgrounds)
- [ ] If Pillow fallback used — verify gradient readability and text centering
- [ ] Twitter thread is 4 tweets, each ≤ 280 characters
- [ ] LinkedIn title ≤ 55 characters
- [ ] Medium title ≤ 55 characters + 5 Topics provided
- [ ] Social_Package.md saved to {{Book_Folder}}/output/social/
- [ ] medium_article_{{slug}}.md saved to {{Book_Folder}}/output/social/ (separate file for import)
- [ ] linkedin_article_{{slug}}.md saved to {{Book_Folder}}/output/social/ (separate file for import)
- [ ] All Amazon links use direct format: `https://www.amazon.com/dp/{{ASIN}}`
- [ ] All Free Chapter links use: `https://michaelrodriguezbooks.com/books/free-chapter-{{book-slug}}/`

---

## COMMUNICATION RULES

- Speak **Russian** with user
- Write **ALL** posts and articles in **English** (including Telegram)
- Stop after image generation (Stage 1) and ask: «Идём дальше?»
- Stop after all posts written and ask user to review before saving package
- If Gemini image generation fails — note it and continue with posts
- Do NOT invent store links or ISBNs — use only what was extracted