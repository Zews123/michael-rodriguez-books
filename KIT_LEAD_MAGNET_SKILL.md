# SKILL: Kit Lead Magnet — Free Chapter Funnel
**Role:** Publishing Agent (Stage 2)  
**Mission:** Create a gated lead magnet on the free-chapter page: visitor reads Introduction → subscribes with email → instantly downloads Chapter 1 as EPUB.  
**Result:** New subscriber in Kit (active, tagged) + EPUB download delivered without any manual steps.

---

## PROBLEM STATEMENT

The old approach put 2–3 full chapters directly on the free-chapter page. This gave away too much content and provided no subscriber capture mechanism — just a generic Kit newsletter embed at the bottom.

**New approach (this skill):**
1. Page shows **only the Introduction** (the hook — ~2,500 words)
2. At the bottom: custom email form → Kit API subscribe → instant EPUB download reveal
3. EPUB contains **Introduction + Chapter 1** only (gated content)
4. Subscriber is immediately **active** in Kit with a book-specific tag

This converts readers into email subscribers before they access Chapter 1.

---

## ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────┐
│  free-chapter-{{book-slug}}.md                                      │
│                                                                     │
│  ┌─────────────────────────────────┐                                │
│  │  Full INTRODUCTION text          │  ← Free, visible to everyone  │
│  │  (~2,500 words — the hook)       │                                │
│  └─────────────────────────────────┘                                │
│                                                                     │
│  ┌─────────────────────────────────┐                                │
│  │  CTA Block (dark gradient)       │                                │
│  │                                  │                                │
│  │  [email input] [Subscribe btn]   │  ← Custom HTML form            │
│  │         │                        │                                │
│  │         ▼  JS fetch()            │                                │
│  │  POST /v3/tags/{id}/subscribe    │  ← Kit API (tag-based)         │
│  │         │                        │                                │
│  │         ▼  on success            │                                │
│  │  [Hide form, show download btn]  │  ← Instant EPUB download       │
│  │                                  │                                │
│  │  [Buy Full Book on Amazon]       │  ← Always visible              │
│  └─────────────────────────────────┘                                │
│                                                                     │
│  EPUB file: /assets/downloads/{{BookName}}_Chapter1.epub             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## STEP 1 — CREATE KIT TAG FOR THE BOOK

Each book gets its own tag in Kit. Use the API to create it.

```bash
curl -s -X POST "https://api.convertkit.com/v3/tags" \
  -H "Content-Type: application/json" \
  -d '{"api_secret":"{{API_SECRET}}","tag":{"name":"{{book-slug}}"}}' \
  | python3 -m json.tool
```

**Response:**
```json
{
    "id": 16990751,
    "name": "countdown-2040",
    "created_at": "2026-03-04T..."
}
```

Save the returned `id` — you'll need it for the JavaScript form.

> ⚠️ **API secret** is required for tag creation. Get it from the user or from previous session context.  
> The `api_key` (public) is sufficient for subscribe calls and is safe to embed in client-side JS.

### Existing tags (reference):
| Tag name | ID | Book |
|----------|-----|------|
| countdown-2040 | 16990751 | Countdown to Collapse |
| shadows-of-power | 16414889 | Shadows of Power |
| rigged-game | 16414924 | Rigged Game |
| warren-buffett | 16414923 | Warren Buffett |
| free-chapter-reader | 16414887 | Generic |
| new-subscriber | 16414886 | Generic |

---

## STEP 2 — GENERATE CHAPTER 1 EPUB

Extract Introduction + Chapter 1 from the book source.

### 2a. Find the source content

```bash
# Find chapter boundaries
grep -n "^#" /Users/zews/Book/{{ProjectName}}/output/Full_Book.md | head -20
```

Look for:
- INTRODUCTION start line
- Chapter 1 start line
- Chapter 2 start line (this is your end boundary)

### 2b. Extract to lead magnet source

```bash
# Extract Introduction + Chapter 1 (from line X to line Y-1)
head -{{CHAPTER_2_START_LINE_MINUS_1}} /Users/zews/Book/{{ProjectName}}/output/Full_Book.md \
  | tail -n +{{INTRO_START_LINE}} > /Users/zews/Book/{{ProjectName}}/output/Chapter1_Lead_Magnet.md
```

### 2c. Add YAML header and CTA footer

Prepend YAML:
```yaml
---
title: "{{BOOK_TITLE}} — Free Chapter"
author: "Michael Rodriguez"
lang: en
---
```

Append CTA at end:
```markdown

## Continue Reading

**You've just finished the Introduction and Chapter 1 of *{{BOOK_TITLE}}*.**

{{2-3 sentences teasing what comes next in Chapter 2.}}

**Get the full book:**

- 📖 [Amazon Kindle & Paperback]({{AMAZON_LINK}})
- 📱 [Apple Books]({{APPLE_LINK}})
- 📚 [Barnes & Noble]({{BN_LINK}})
- 📕 [Kobo]({{KOBO_LINK}})

*© {{YEAR}} Michael Rodriguez. All rights reserved.*
```

### 2d. Generate EPUB via pandoc

```bash
pandoc /Users/zews/Book/{{ProjectName}}/output/Chapter1_Lead_Magnet.md \
  -o /Users/zews/Book/michael-rodriguez-books/assets/downloads/{{BookName}}_Chapter1.epub \
  --metadata title="{{BOOK_TITLE}} — Free Chapter" \
  --metadata author="Michael Rodriguez"
```

Verify:
```bash
ls -la /Users/zews/Book/michael-rodriguez-books/assets/downloads/{{BookName}}_Chapter1.epub
# Expected size: 15–25 KB for Introduction + 1 chapter
```

> ⚠️ **pandoc** must be installed: `/opt/homebrew/bin/pandoc`  
> If not available: `brew install pandoc`

---

## STEP 3 — BUILD THE FREE-CHAPTER PAGE

### Page structure

The page has 3 sections:
1. **Introduction text** — full, unabridged (~2,500 words)
2. **Lead magnet CTA block** — email form + gated download
3. **Back link** — to the book page

### 3a. YAML front matter

```yaml
---
layout: default
title: "Free Chapter — {{BOOK_TITLE}} by Michael Rodriguez"
description: "Read the Introduction of {{BOOK_TITLE}} free. Subscribe to get Chapter 1 as EPUB."
canonical_url: "https://michaelrodriguezbooks.com/books/free-chapter-{{book-slug}}"
image: "https://michaelrodriguezbooks.com/assets/images/{{BookName}}.webp"
---
```

> ⚠️ **No trailing slash** in canonical_url — GitHub Pages returns 404 with trailing slashes.

### 3b. Introduction section

```markdown
# {{BOOK_TITLE}} — Free Preview

**Read the full Introduction below.** {{One-sentence hook}}. Subscribe below to get Chapter 1 free.

<img src="{{ site.baseurl }}/assets/images/{{BookName}}.webp" alt="{{BOOK_TITLE}} by Michael Rodriguez" style="width: 220px; height: auto; float: right; margin: 0 0 20px 20px; border-radius: 8px;">

---

## INTRODUCTION — {{Introduction Title}}

{{Full Introduction text — copy from Full_Book.md, keep all formatting}}

---
```

### 3c. Lead magnet CTA block (TEMPLATE — copy and customize)

```html
<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 35px; border-radius: 12px; margin: 40px 0; border: 2px solid #c9a227; text-align: center;">
  <h2 style="color: #c9a227; margin-top: 0;">📖 Want to read Chapter 1? Get it free.</h2>
  <p style="color: #e8e6e3; font-size: 1.1rem; margin-bottom: 5px;"><strong>Chapter 1: {{CHAPTER_1_TITLE}}</strong> — {{one-sentence chapter description}}.</p>
  <p style="color: #999; font-size: 0.95rem; margin-bottom: 20px;">Enter your email below — receive Chapter 1 as EPUB instantly.</p>

  <div id="lead-form">
    <form id="part1-form" style="display:inline-flex;gap:10px;flex-wrap:wrap;justify-content:center;">
      <input type="email" id="lead-email" placeholder="your@email.com" required
        style="padding:12px 18px;border-radius:6px;border:1px solid #555;background:#111;color:#fff;font-size:1rem;width:260px;">
      <button type="submit" id="lead-btn"
        style="background:#c9a227;color:#000;font-weight:700;padding:12px 24px;border-radius:6px;border:none;font-size:1rem;cursor:pointer;">
        Send me Chapter 1
      </button>
    </form>
    <p id="lead-error" style="color:#ff6347;margin-top:10px;display:none;"></p>
  </div>

  <div id="lead-success" style="display:none;">
    <p style="color:#4ade80;font-size:1.2rem;font-weight:700;margin-bottom:15px;">✅ You're in! Download your free Chapter 1:</p>
    <a href="{{ site.baseurl }}/assets/downloads/{{BookName}}_Chapter1.epub"
       style="background:#4ade80;color:#000;font-weight:700;padding:14px 28px;font-size:1.1rem;border-radius:8px;text-decoration:none;display:inline-block;"
       download>📥 Download EPUB</a>
    <p style="color:#999;font-size:0.85rem;margin-top:12px;">Check your inbox for a confirmation from Michael Rodriguez Books.</p>
  </div>

  <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid #333;">
    <p style="color: #999; font-size: 0.9rem; margin-bottom: 10px;">Already read Chapter 1? Get the full book:</p>
    <a href="{{AMAZON_LINK}}" class="btn" style="background: #ff9900; color: #000; font-weight: 700; padding: 14px 28px; font-size: 1.1rem; border-radius: 8px; text-decoration: none; display: inline-block;">Buy Full Book on Amazon</a>
  </div>
</div>
```

### 3d. JavaScript — Kit API subscribe (TEMPLATE)

```html
<script>
document.getElementById('part1-form').addEventListener('submit', function(e) {
  e.preventDefault();
  var email = document.getElementById('lead-email').value;
  var btn = document.getElementById('lead-btn');
  var errEl = document.getElementById('lead-error');
  btn.disabled = true;
  btn.textContent = 'Sending...';
  errEl.style.display = 'none';
  fetch('https://api.convertkit.com/v3/tags/{{TAG_ID}}/subscribe', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({api_key: '{{API_KEY}}', email: email})
  })
  .then(function(r) { return r.json(); })
  .then(function(data) {
    if (data.subscription) {
      document.getElementById('lead-form').style.display = 'none';
      document.getElementById('lead-success').style.display = 'block';
    } else {
      errEl.textContent = 'Something went wrong. Please try again.';
      errEl.style.display = 'block';
      btn.disabled = false;
      btn.textContent = 'Send me Chapter 1';
    }
  })
  .catch(function() {
    errEl.textContent = 'Network error. Please try again.';
    errEl.style.display = 'block';
    btn.disabled = false;
    btn.textContent = 'Send me Chapter 1';
  });
});
</script>
```

### 3e. Footer

```html
<a href="{{ site.baseurl }}/books/{{book-slug}}" style="color: #c9a227;">&larr; Back to {{BOOK_TITLE}}</a>

<style>
.btn:hover { opacity: 0.9; }
h2, h3 { color: #c9a227; }
p { line-height: 1.8; }
blockquote { border-left: 3px solid #c9a227; padding-left: 20px; color: #999; font-style: italic; }
</style>
```

---

## STEP 4 — VERIFY

### 4a. Test Kit subscription via API

```bash
# Test with a disposable email
curl -s -X POST https://api.convertkit.com/v3/tags/{{TAG_ID}}/subscribe \
  -H "Content-Type: application/json" \
  -d '{"api_key":"{{API_KEY}}","email":"test@example.com"}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('state:', d.get('subscription',{}).get('state','FAILED'))"
```

**Expected:** `state: active`

> ⚠️ If state is `inactive` — you're using form-based subscribe instead of tag-based. Tag-based always returns `active`.

### 4b. Verify EPUB is accessible

```bash
curl -s -o /dev/null -w "%{http_code} %{size_download}" \
  https://michaelrodriguezbooks.com/assets/downloads/{{BookName}}_Chapter1.epub
```

**Expected:** `200 XXXXX` (HTTP 200 + file size in bytes)

### 4c. Clean up test subscriber

```bash
# Find and unsubscribe test email
curl -s "https://api.convertkit.com/v3/subscribers?api_secret={{API_SECRET}}&email_address=test@example.com" \
  | python3 -c "import json,sys; [print(s['id']) for s in json.load(sys.stdin).get('subscribers',[])]" \
  | while read sid; do
    curl -s -X PUT "https://api.convertkit.com/v3/subscribers/$sid/unsubscribe" \
      -H "Content-Type: application/json" \
      -d "{\"api_secret\":\"{{API_SECRET}}\"}"
  done
```

---

## CRITICAL: TAG-BASED vs FORM-BASED SUBSCRIBE

| | Form-based | Tag-based ✅ |
|---|---|---|
| Endpoint | `POST /v3/forms/{id}/subscribe` | `POST /v3/tags/{id}/subscribe` |
| Subscriber state | `inactive` (double opt-in) | **`active`** (immediate) |
| Appears in Subscribers? | ❌ Not until confirmed | ✅ Immediately |
| Requires api_secret? | No (api_key works) | No (api_key works) |
| Safe for client-side JS? | Yes | **Yes** |
| Creates tag? | No (needs separate call) | **Yes** (auto-tagged) |

**Always use tag-based subscribe for lead magnets.** It's one API call, immediately active, and auto-tags the subscriber.

---

## CRITICAL: NO TRAILING SLASHES

GitHub Pages returns **404** for URLs with trailing slashes. All `canonical_url` values must end WITHOUT `/`.

```yaml
# ✅ CORRECT
canonical_url: "https://michaelrodriguezbooks.com/books/free-chapter-countdown-2040"

# ❌ WRONG — will 404
canonical_url: "https://michaelrodriguezbooks.com/books/free-chapter-countdown-2040/"
```

---

## KIT API REFERENCE (QUICK)

**Base URL:** `https://api.convertkit.com/v3/`

| Action | Method | Endpoint | Auth |
|--------|--------|----------|------|
| List tags | GET | `/tags?api_key=...` | api_key |
| Create tag | POST | `/tags` | api_secret (body) |
| Subscribe + tag | POST | `/tags/{id}/subscribe` | api_key (body) |
| List subscribers | GET | `/subscribers?api_secret=...` | api_secret |
| Unsubscribe | PUT | `/subscribers/{id}/unsubscribe` | api_secret (body) |

**Kit API key (public):** `PboITVh5dkI7c25JFX2Qsw`  
**Kit form UID (general newsletter):** `b2a1614bc4`

> ⚠️ API v3 does NOT support: form creation, incentive email setup, file uploads (UI-only features).  
> ⚠️ API v4 requires OAuth (browser-based auth flow) — not usable from CLI.

---

## VARIABLES CHECKLIST

Before building, collect these values:

```
{{book-slug}}          — URL slug (e.g., "countdown-2040")
{{BookName}}           — File prefix (e.g., "Countdown_2040")
{{BOOK_TITLE}}         — Full title (e.g., "Countdown to Collapse: The 2040 Crisis")
{{CHAPTER_1_TITLE}}    — Chapter 1 heading (e.g., "The Graveyard of Greatness")
{{TAG_ID}}             — Kit tag ID (create via Step 1)
{{API_KEY}}            — Kit public API key
{{API_SECRET}}         — Kit API secret (for tag creation + cleanup only)
{{AMAZON_LINK}}        — Amazon product URL
{{APPLE_LINK}}         — Apple Books URL
{{BN_LINK}}            — Barnes & Noble URL
{{KOBO_LINK}}          — Kobo URL
{{INTRO_START_LINE}}   — Line number in Full_Book.md
{{CHAPTER_2_START_LINE_MINUS_1}} — End of Chapter 1
```

---

## OUTPUT DELIVERABLES

After running this skill:

1. **Kit tag created** — with book-specific name, ID saved
2. **EPUB file** — `assets/downloads/{{BookName}}_Chapter1.epub` (15–25 KB)
3. **Free-chapter page** — `books/free-chapter-{{book-slug}}.md` with:
   - Full Introduction text (the hook)
   - Custom JS form → Kit tag subscribe → instant EPUB download
   - Amazon buy CTA
4. **Lead magnet source** — `{{ProjectName}}/output/Chapter1_Lead_Magnet.md`
5. **Test passed** — API returns `state: active`, EPUB returns HTTP 200
