# ADD NEW BOOK TO WEBSITE — Agent Prompt

## LAUNCH INSTRUCTION

User provides only:
- Path to the book folder (e.g. `/Users/zews/Book/Writers_Agent/Shadows_of_Power/`)
- Store links (Amazon, Apple Books, Kobo, Barnes & Noble)
- ISBN Hardcover + ISBN eBook

Everything else — extract automatically from the files.

---

## STAGE 0 — EXTRACT BOOK DATA FROM FILES

Read the following files from the book folder:

### From `output/Final_Book.docx` — extract:
- Book title
- Subtitle (if present)
- Author name
- Publisher name and cities
- Edition / publication date
- Copyright year
- Book description / About the Book text
- Chapter titles (for What You'll Discover section)
- Key themes and insights (for Key Revelations section)

### From `output/Publishing_Package.txt` — extract:
- Long book description (SEO-ready)
- Short book description
- Keywords list
- Author bio
- Taglines

### Cover image:
- Look for files matching `Cover_*.png` or `Cover_*.webp` in `output/`
- If multiple covers exist — show the user thumbnails and ask which one to use
- Convert chosen file to `.webp` if not already

> Report all extracted data to the user in a structured summary before proceeding.
> If any critical field is missing — ask the user to provide it.

---

## STAGE 1 — ANALYZE EXISTING SITE STRUCTURE

Before writing any code:

1. Read the GitHub repo at: `https://michaelrodriguezbooks.com/`
2. Find the most recently added book on the site
3. Open that book's `.md` file as reference template
4. Also open the most recent blog post in `blog/` folder as blog reference template
5. Document:
   - YAML front matter structure (book page)
   - SEO blocks (canonical, schema, OG, Twitter Cards)
   - JSON-LD `@graph` structure
   - Button styles and classes
   - Image path format
   - Card format in `index.md` and `books/index.md`
   - Entry format in `about.md`
   - Blog post structure (FAQ format, CSS, schema, social share block)

> Do NOT proceed until analysis is complete. Report findings.

---

## STAGE 2 — PREPARE COVER IMAGE

1. Take the selected cover from `output/`
2. Convert to `.webp` if needed
3. Name it based on book title: `{{Book_Title_Slug}}.webp`
4. Save to: `assets/images/{{filename}}.webp` in the GitHub repo
5. Confirm file is in place

---

## STAGE 3 — CREATE BOOK PAGE

Create: `books/{{book-slug}}.md`

Use the reference template from Stage 1. Replace all content with extracted data.

### YAML front matter:
```yaml
---
layout: default
title: "{{BOOK_TITLE}} | Michael Rodriguez"     # STRICT: max 58 characters
description: "{{SHORT_DESCRIPTION}}"            # max 150 characters
canonical_url: "https://michaelrodriguezbooks.com/books/{{book-slug}}"
image: "https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp"
date: {{YYYY-MM-DD}}                              # REQUIRED for Jekyll sorting and Schema
---
```

### Performance block:
```html
<link rel="preload" href="https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp" as="image" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://www.amazon.com">
<link rel="dns-prefetch" href="https://www.amazon.com">
```

### Critical CSS (inline, minified):
```html
<style>
.book-btn{background:#1a3c65;color:#fff;padding:10px 16px;border-radius:6px;text-decoration:none;font-weight:700;display:inline-block;text-align:center;min-width:110px;border:0}.book-btn:hover{text-decoration:none;color:#fff;opacity:0.9}.book-btn-amazon{background:#ff9900}.book-btn-apple{background:#000}.book-btn-kobo{background:#1e90ff}.book-btn-bn{background:#2e8b57}.book-btn-smash{background:#ff6347}.book-buttons{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:15px}@media (max-width:768px){.book-buttons{flex-direction:column}.book-btn{width:100%;margin-bottom:5px}}
</style>
```

### Open Graph + Twitter Cards:
```html
<meta property="og:type" content="book">
<meta property="og:title" content="{{BOOK_TITLE}}">
<meta property="og:description" content="{{SHORT_DESCRIPTION}}">
<meta property="og:image" content="https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp">
<meta property="og:image:width" content="400">
<meta property="og:image:height" content="600">
<meta property="og:url" content="https://michaelrodriguezbooks.com/books/{{book-slug}}">
<meta property="og:site_name" content="Michael Rodriguez Books">
<meta property="book:author" content="Michael Rodriguez">
<meta property="book:isbn" content="{{ISBN_EBOOK}}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{BOOK_TITLE}}">
<meta name="twitter:description" content="{{SHORT_DESCRIPTION}}">
<meta name="twitter:image" content="https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp">
<meta name="twitter:creator" content="@MRodriguezBooks">
```

### JSON-LD Schema (`@graph` — three nodes):
- `WebPage` node: url, name, datePublished, dateModified
- `Book` node: title, author, both ISBNs, publisher, genre, offers (Amazon link)
- `FAQPage` node: 4 questions based on book's actual content

### Content sections (in this order):

**0. Publication info** — from extracted data:
```
By {{AUTHOR_NAME}}
{{EDITION}}
Published by {{PUBLISHER}}
{{PUBLISHER_CITIES}}
ISBN: {{ISBN_HARDCOVER}} (Hardcover)
ISBN: {{ISBN_EBOOK}} (eBook)
```

**1. About the Book**
- Open with Herman Hook method (provocative, emotional, unexpected angle)
- SEO-optimized, high-frequency keywords from `Publishing_Package.txt`

**2. What You'll Discover** — 6 blocks with contextual emojis
- Build from chapter titles and themes extracted from `Final_Book.docx`

**3. Key Revelations** — 4–6 punchy insights from book content

**4. About the Author** — from `Publishing_Package.txt` author bio

**5. Get Your Copy Today**
- Amazon, Apple Books, Kobo, Barnes & Noble buttons (user-provided links)
- Libraries: OverDrive, Hoopla, BorrowBox (copy style from reference)

**6. Free Chapter Banner** (insert BEFORE "About the Book"):
```html
<div style="background: linear-gradient(135deg, #1a3c65 0%, #0d253f 100%); padding: 20px 25px; border-radius: 10px; margin: 20px 0; border: 1px solid #c9a227; text-align: center;">
  <a href="{{ site.baseurl }}/books/free-chapter-{{book-slug}}" style="color: #c9a227; font-size: 1.2rem; font-weight: 700;">📖 Read First 2 Chapters FREE →</a>
</div>
```

**7. Share This Book** — copy from reference template exactly

**8. Subscribe to Newsletter** — embed Kit form:
```html
<script async data-uid="b2a1614bc4" src="https://michael-rodriguez.kit.com/b2a1614bc4/index.js"></script>
```

### Image tag:
```html
<img src="https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp"
     alt="{{BOOK_TITLE}} by Michael Rodriguez — book cover"
     width="400" height="600"
     loading="lazy" decoding="async">
```

---

## STAGE 3.5 — CREATE FREE CHAPTER PAGE (Lead Magnet)

**Skill file:** `/Users/zews/Book/KIT_LEAD_MAGNET_SKILL.md`

Read and follow `KIT_LEAD_MAGNET_SKILL.md` completely. It contains:
- Full page template (HTML + JS)
- Kit API tag creation via CLI
- EPUB generation via pandoc
- Tag-based subscribe (immediate active — no double opt-in)
- Testing and verification steps

### Summary of what the skill builds:

Create: `books/free-chapter-{{book-slug}}.md`

1. Page shows **only the full Introduction** (~2,500 words) — this is the hook
2. At the bottom: **custom JS email form** → Kit API tag subscribe → **instant EPUB download reveal**
3. EPUB contains **Introduction + Chapter 1** (generated via pandoc, saved to `assets/downloads/`)
4. Subscriber is immediately **active** in Kit with a book-specific tag
5. Amazon buy CTA always visible below the form

### Key technical decisions:
- **Tag-based subscribe** (not form-based) — subscriber is `active` immediately, no double opt-in
- **api_key in JS is safe** — it's a public key, can only subscribe people
- **EPUB URL is technically public** but undiscoverable without subscribing — standard lead magnet pattern

### Commit:
```bash
git add books/free-chapter-{{book-slug}}.md assets/downloads/
git commit -m "Add free chapter lead magnet for {{BOOK_TITLE}}"
```

---

## STAGE 4 — CREATE FAQ BLOG POST

Create: `blog/{{book-slug}}-faq.html`

> ⚠️ **CRITICAL: `.html` files in Jekyll do NOT process Markdown.**
> Since blog posts use `.html` extension, ALL content MUST be written in **pure HTML**.
> Do NOT use Markdown syntax (`#`, `##`, `*`, `**`, `-` for lists).
> Use `<h1>`, `<h2>`, `<p>`, `<strong>`, `<ul><li>` etc. instead.
> If you write Markdown in an `.html` file, it will render as **raw text** on the site.

The FAQ blog post creates a semantic SEO cluster around the book page.  
It targets long-tail search queries that the book page itself doesn't cover.

Use the most recent blog post in `blog/` as structural reference.

### YAML front matter:
```yaml
---
layout: default
title: "{{FAQ_TITLE}}"                          # Question-format title, max 58 chars
description: "{{FAQ_DESCRIPTION}}"             # max 150 characters
canonical_url: "https://michaelrodriguezbooks.com/blog/{{book-slug}}-faq.html"
image: "https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp"
date: {{YYYY-MM-DD}}                              # REQUIRED for Jekyll sorting
---
```

> `FAQ_TITLE` — generate as a compelling question based on book's main theme.
> Example: *"Why Do Smart People Stay Poor? The Intelligence-Wealth Paradox FAQ"*

### Blog post structure:

**Performance + OG + Twitter** — same pattern as book page, `og:type` = `article`

**Critical CSS** — copy from reference blog post (includes typography: Georgia serif, drop cap `.first-letter`, h2 with left border)

**Required blog Critical CSS block** (inline in `<style>`, adapt colors):
```html
<style>
body{font-family:Georgia,'Times New Roman',serif;line-height:1.8;color:#e8e6e3}
h1{font-size:2.2rem;line-height:1.3;background:linear-gradient(135deg,#c9a227,#e8d48b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
h2{color:#c9a227;margin-top:2rem;padding-left:15px;border-left:4px solid #c9a227}
.date{color:#999;font-style:italic;margin-bottom:2rem}
.first-letter::first-letter{font-size:3.5em;float:left;line-height:0.8;padding-right:8px;color:#c9a227;font-weight:bold}
.highlight-box{background:#1a1a2e;border-left:4px solid #c9a227;padding:20px 25px;margin:25px 0;border-radius:0 8px 8px 0;font-style:italic}
.cta-box{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);padding:30px;border-radius:12px;margin:30px 0;border:2px solid #c9a227;text-align:center}
</style>
```

**Required blog content elements** (all in pure HTML):
1. `<h1>` title
2. `<p class="date">` — date + "By Michael Rodriguez"
3. `<p class="first-letter">` — opening paragraph (drop cap via CSS)
4. `<h2>` sections with `<p>` paragraphs
5. `<div class="highlight-box">` — pull quotes from book
6. CTA box with dual buttons
7. **"Available Now" product showcase** (see template below)
8. `<blockquote>` — "About this Investigation" note
9. Share buttons with inline SVG icons (Twitter, Facebook, LinkedIn, Reddit)
10. Related Articles + Related Books sections
11. Newsletter Kit form
12. `<p><a href="{{ site.baseurl }}/blog">← Back to Blog</a></p>`

**Do NOT include** `@import url(Google Fonts)` anywhere — it blocks rendering. Preconnect in head is sufficient.

**Content — 7 FAQ questions:**
- Generate questions based on book themes, chapter titles, and keywords from `Publishing_Package.txt`
- Each question: target a specific long-tail search query readers would Google
- Each answer: 3–5 paragraphs, keyword-rich, reference book with internal link
- Q1: General "What is [main theme] about?"
- Q2–Q6: Specific angles, revelations, concepts from the book
- Q7: Actionable — "What should readers do first?"

**Internal links to book page** — link to `books/{{book-slug}}.md` at least 4 times naturally within answer text

**FAQPage JSON-LD schema** — all 7 questions, answers 2–4 sentences each

**CTA box** — dual buttons (Amazon + Free Chapter):
```html
<div class="cta-box">
  <h3>📖 Get the Full Story</h3>
  <a href="{{AMAZON_DIRECT_LINK}}" class="btn-amazon">📦 Buy on Amazon</a>
  <a href="{{ site.baseurl }}/books/free-chapter-{{book-slug}}" class="btn-free">📖 Read Free Chapter</a>
</div>
```

**Related Articles** — link to 2–3 other blog posts on related topics:
```html
<h3>📚 Related Articles</h3>
<ul>
  <li><a href="{{ site.baseurl }}/blog/{{related-slug-1}}">{{Related Title 1}}</a></li>
  <li><a href="{{ site.baseurl }}/blog/{{related-slug-2}}">{{Related Title 2}}</a></li>
</ul>
```

**Related Books** — link to 2–3 related books from the catalog:
```html
<h3>📕 Related Books</h3>
<ul>
  <li><a href="{{ site.baseurl }}/books/{{related-book-slug}}">{{Related Book Title}}</a></li>
</ul>
```

**"Available Now" product showcase** — dark grid block with 3D cover + store buttons + metadata:
```html
<div style="background:#1a1a2e;padding:40px 30px;border-radius:12px;margin:40px 0;border:1px solid #c9a22733">
  <h2 style="text-align:center;border:none;padding:0">📚 Available Now</h2>
  <div style="display:grid;grid-template-columns:250px 1fr;gap:30px;align-items:start;margin-top:20px">
    <div style="text-align:center">
      <img src="https://michaelrodriguezbooks.com/assets/images/{{3D_cover}}.webp"
           alt="{{BOOK_TITLE}}" width="250" loading="lazy" decoding="async"
           style="border-radius:8px;box-shadow:0 8px 32px rgba(0,0,0,0.4)">
    </div>
    <div>
      <h3 style="color:#c9a227;margin-top:0">{{BOOK_TITLE}}</h3>
      <p>{{SHORT_DESCRIPTION}}</p>
      <div style="display:flex;flex-wrap:wrap;gap:10px;margin:20px 0">
        <a href="{{AMAZON_LINK}}" style="background:#ff9900;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:700">📦 Amazon</a>
        <a href="{{APPLE_LINK}}" style="background:#000;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:700">🍎 Apple Books</a>
        <a href="{{KOBO_LINK}}" style="background:#1e90ff;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:700">📖 Kobo</a>
        <a href="{{BN_LINK}}" style="background:#2e8b57;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:700">📗 Barnes & Noble</a>
      </div>
      <p style="color:#999;font-size:0.9rem">ISBN: {{ISBN_EBOOK}} (eBook) · {{ISBN_HARDCOVER}} (Hardcover)<br>Publisher: Resource Economics Press</p>
      <p style="color:#999;font-size:0.85rem">Also available at libraries via OverDrive, Hoopla, BorrowBox</p>
    </div>
  </div>
</div>
```

> Use the 3D cover image (not flat cover) in this block. If user provided 3D images, convert to `.webp` and use here.

**Subscribe to Newsletter** — Kit form embed:
```html
<script async data-uid="b2a1614bc4" src="https://michael-rodriguez.kit.com/b2a1614bc4/index.js"></script>
```

**Share This Article block** — social share buttons (Twitter, Facebook, LinkedIn, Reddit)

**Non-critical CSS** — move to end of document (after all content), same as reference blog

### Blog post commit:
```bash
git add blog/{{book-slug}}-faq.html
git commit -m "Add FAQ blog post for {{BOOK_TITLE}}"
```

---

## STAGE 4.5 — CREATE DEEP-DIVE ANALYTICAL BLOG POST

Create: `blog/{{analytical-slug}}.html`

> ⚠️ **CRITICAL: `.html` files in Jekyll do NOT process Markdown.**
> ALL content MUST be written in **pure HTML** (`<h1>`, `<h2>`, `<p>`, `<strong>`, etc.).
> Do NOT use Markdown syntax. Copy the exact CSS and structural patterns from Stage 4 above.

This is a **long-form analytical article** (2500–3500 words) that dives deep into a specific aspect of the book's subject matter. It uses original research data from the manuscript to create unique SEO-worthy content.

### Purpose:
- Attract organic Google traffic via informational queries
- Demonstrate author expertise and book depth
- Create second content pillar around the book (FAQ = pillar 1, deep-dive = pillar 2)

### YAML front matter:
```yaml
---
layout: default
title: "{{ANALYTICAL_TITLE}}"                   # Descriptive, keyword-rich, max 58 chars
description: "{{ANALYTICAL_DESCRIPTION}}"       # max 150 characters
image: "https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp"
canonical_url: "https://michaelrodriguezbooks.com/blog/{{analytical-slug}}.html"
date: {{YYYY-MM-DD}}
---
```

### Article structure:
1. **BlogPosting JSON-LD Schema** — include `headline`, `description`, `image`, `author` (Person), `publisher` (Organization), `datePublished`, `dateModified`, `wordCount`, `inLanguage`, `keywords[]`
2. **Performance + OG + Twitter** — `og:type` = `article`
3. **H1 title** + date + author byline
4. **Opening** — Herman Hook (provocative fact/statistic from the manuscript)
5. **4–6 H2 sections** — deep analytical content, using specific data, quotes, timelines, and facts from `output/Final_Book.docx`
6. **Blockquotes** — pull actual quotes from the manuscript
7. **CTA box** — dual buttons: Amazon + Free Chapter
8. **Related Articles** — links to FAQ post and 1–2 other blog posts
9. **Related Books** — links to 2–3 related books from catalog
10. **Newsletter Kit form** embed
11. **Social share buttons** (Twitter, Facebook, LinkedIn, Reddit)
12. **Back to Blog** link

### Key principles:
- Content must be **original analysis**, not a summary. Pull specific facts, dates, names, statistics from the manuscript
- Use `<blockquote>` for actual book quotes
- Include `.highlight-box` or `.timeline` CSS components for visual richness
- Target informational search queries, not just the book title

### Commit:
```bash
git add blog/{{analytical-slug}}.html
git commit -m "Add deep-dive article for {{BOOK_TITLE}}"
```

---

## STAGE 5 — UPDATE INDEX PAGES

### `index.md` — insert new book card **first**, keep all existing cards
### `books/index.md` — insert new book card **first**, with **Free Chapter** button:
```html
<div class="book-card">
  <img src="{{ site.baseurl }}/assets/images/{{filename}}.webp" alt="{{BOOK_TITLE}} by Michael Rodriguez">
  <div class="book-card-content">
    <h3>{{BOOK_TITLE}}</h3>
    <p>{{SHORT_DESCRIPTION}}</p>
    <a href="{{ site.baseurl }}/books/free-chapter-{{book-slug}}" class="btn" style="background: #2e8b57; margin-right: 8px;">Free Chapter</a>
    <a href="{{ site.baseurl }}/books/{{book-slug}}" class="btn">Read More…</a>
  </div>
</div>
```

### `blog.md` — TWO new blog post cards (FAQ + analytical article):
- Insert both as first `<div class="blog-card">` entries
- Also add BlogPosting entries to the JSON-LD Schema `@graph` array in `blog.md`:
```json
{
  "@type": "BlogPosting",
  "headline": "{{BLOG_POST_TITLE}}",
  "url": "https://michaelrodriguezbooks.com/blog/{{post-slug}}/",
  "datePublished": "{{YYYY-MM-DD}}",
  "author": { "@type": "Person", "name": "Michael Rodriguez" }
}
```

### `books/index.md` Schema — add new Book to the JSON-LD `@graph` array in books/index.md

Match card format exactly to existing cards.

> **IMPORTANT:** `blog.md` is the blog index page. After creating both blog posts (Stages 4 + 4.5), you MUST add their cards to `blog.md` as the first entries. Without this, the posts won't appear on the blog listing page even though the direct URLs work.

```bash
git add index.md books/index.md blog.md
git commit -m "Update index pages: add {{BOOK_TITLE}} card"
```

---

## STAGE 5.5 — UPDATE HOMEPAGE LAYOUT

The homepage uses a custom layout: `_layouts/homepage.html`  
It has TWO book sections that must be updated when a new book is published:

### 1. "Featured Investigation" block → replace with new book

Find the `<div class="featured-book reveal">` block and replace it entirely:
- Cover image → new book's `.webp` cover
- `featured-book-year` → current year + "Investigation"
- `featured-book-title` → new book title
- `featured-book-subtitle` → subtitle or hook line
- `featured-book-desc` → 2–3 sentence description
- `btn-primary` link → new book page URL

### 2. "Investigations & Exposés" grid → add NEW book card

- Add the **NEW book** as the **FIRST** `<a class="book-card reveal">` entry in the `<div class="books-grid">` section (the new book must appear in BOTH the Featured block AND the grid)
- The previous Featured book stays as the second card (it was already first in the grid)
- **Remove the LAST card** from the grid (to keep the grid at ~9–10 cards max)

### 3. Hero visual section → update first book cover

Find the `<div class="hero-visual">` block (4 book covers in the hero banner):
- Replace the **first** `<div class="hero-book">` image with the new book's cover
- Move the previous first cover to the **second** position
- Remove the previous second cover (keep total at 4)

### 4. Preload tag → update for new book image

Find `<link rel="preload" ... as="image">` near the top of `homepage.html` and change to new book's cover URL.

### Summary of rotation logic:

```
NEW BOOK → Featured Investigation (replaces previous)
NEW BOOK → ALSO first card in Investigations grid
LAST CARD in grid → Removed (keeps grid at ~9–10)
Hero covers: [NEW, prev_1st, prev_3rd, prev_4th]
Preload: NEW book cover
```

```bash
git add _layouts/homepage.html
git commit -m "Homepage: {{BOOK_TITLE}} as Featured, rotate grid"
```

---

## STAGE 6 — UPDATE ABOUT PAGE

`about.md` → Publications section → add new book as **first entry**

```bash
git add about.md
git commit -m "Update about page: add {{BOOK_TITLE}}"
```

---

## STAGE 7 — PUSH AND VERIFY

```bash
git push origin main
```

Wait for GitHub Pages rebuild (1–2 min), then verify:
- Book page live: `https://michaelrodriguezbooks.com/books/{{book-slug}}`
- Free Chapter page live: `https://michaelrodriguezbooks.com/books/free-chapter-{{book-slug}}`
- FAQ blog post live: `https://michaelrodriguezbooks.com/blog/{{book-slug}}-faq/`
- Analytical article live: `https://michaelrodriguezbooks.com/blog/{{analytical-slug}}/`
- Cards appear first on index pages
- About page updated

---

## STAGE 8 — VALIDATION CHECKLIST

**Book page:**
- [ ] Title ≤ 58 characters (counted exactly)
- [ ] Description ≤ 150 characters (counted exactly)
- [ ] `date:` field present in YAML front matter
- [ ] og:image is absolute https:// URL
- [ ] Twitter Card present
- [ ] WebPage + Book + FAQPage in @graph schema
- [ ] Both ISBNs in Book schema
- [ ] Preload + preconnect tags present
- [ ] Critical CSS inline in head
- [ ] Image has width/height attributes
- [ ] All 4 store buttons present
- [ ] Libraries section present
- [ ] Free Chapter banner present (links to free-chapter page)
- [ ] Kit newsletter form embedded
- [ ] Social share buttons present

**Free Chapter page:**
- [ ] Contains Introduction + Chapters 1–2 from manuscript
- [ ] Kit form embedded in CTA block
- [ ] Amazon direct link present
- [ ] Back link to book page present
- [ ] Canonical URL set correctly

**FAQ blog post:**
- [ ] Title is a compelling question
- [ ] `date:` field in YAML front matter
- [ ] FAQPage schema with 7 questions
- [ ] At least 4 internal links to book page
- [ ] No `@import url(Google Fonts)` in CSS
- [ ] CTA box with Amazon + Free Chapter dual buttons
- [ ] Related Articles section (2–3 links)
- [ ] Related Books section (2–3 links)
- [ ] Kit newsletter form embedded
- [ ] Share block present

**Analytical blog post:**
- [ ] BlogPosting Schema with all required fields
- [ ] `date:` field in YAML front matter
- [ ] 2500–3500 words of original analytical content
- [ ] Real facts/quotes from manuscript (not generic)
- [ ] CTA box with Amazon + Free Chapter dual buttons
- [ ] Related Articles section
- [ ] Related Books section
- [ ] Kit newsletter form embedded
- [ ] Share block present

**Site structure:**
- [ ] Book card added FIRST in `index.md`
- [ ] Book card with Free Chapter button added FIRST in `books/index.md`
- [ ] Book Schema added to `books/index.md` @graph
- [ ] Both blog post cards added FIRST in `blog.md`
- [ ] Both BlogPosting entries added to `blog.md` @graph Schema
- [ ] Book added FIRST in `about.md` Publications
- [ ] All commits pushed
- [ ] All 4 pages live and verified

**Homepage layout (`_layouts/homepage.html`):**
- [ ] New book in "Featured Investigation" block (cover, title, subtitle, desc, link)
- [ ] Previous featured book moved to FIRST card in "Investigations & Exposés" grid
- [ ] Last card removed from grid (keep 8 cards total)
- [ ] Hero visual: new book cover as first of 4 hero covers
- [ ] Preload tag updated to new book's cover image

---

## COMMUNICATION RULES

- Speak **Russian** with user
- Stop after each Stage and ask: «Идём дальше?»
- If data cannot be extracted automatically — ask user, do not invent
- Show extracted data summary before starting any file creation
-  Before creating book page — read and apply: /Users/zews/Book/GitHub_publishing_agent/SEO_SKILL.md