# SKILL: Book Page & Blog Post SEO
**Role:** SEO Engineer for Jekyll/GitHub Pages book catalog  
**Mission:** Ensure every book page, free chapter page, and blog post is maximally optimized for Google, social platforms, and rich results.  
**Apply this skill** when creating or updating any `.md` or `.html` page on the site.

---

## BLOCK 1 — YAML FRONT MATTER (clean, no junk)

### For book pages (`books/{{book-slug}}.md`):

```yaml
---
layout: default
title: "{{BOOK_TITLE}} | Michael Rodriguez"
description: "{{SEO_DESCRIPTION}}"
canonical_url: "https://michaelrodriguezbooks.com/books/{{book-slug}}"
image: "https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp"
author: "Michael Rodriguez"
date: {{YYYY-MM-DD}}
date_published: "{{YYYY-MM-DD}}"
date_modified: "{{YYYY-MM-DD}}"
---
```

### For blog posts (`blog/{{slug}}.html`):

```yaml
---
layout: default
title: "{{POST_TITLE}}"
description: "{{SEO_DESCRIPTION}}"
canonical_url: "https://michaelrodriguezbooks.com/blog/{{slug}}.html"
image: "https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp"
date: {{YYYY-MM-DD}}
---
```

> ⚠️ The `date:` field is **REQUIRED** for all pages. Jekyll uses it for sorting, and it feeds into Schema `datePublished`. Without it, blog posts may appear in wrong order and Schema will be incomplete.

**Strict rules:**
- `title` — max **58 characters** total (count every character including spaces and `| Michael Rodriguez`)
- `description` — max **150 characters** (count exactly before saving)
- `image` — must be **absolute URL** (starts with `https://`), not `{{ site.baseurl }}/...`
- Do NOT add: `price_kindle`, `pages`, `tags`, `category`, `isbn_*` — Jekyll ignores them in SEO
- `date_modified` — update every time the page is edited

**Auto-check title length (run before saving):**
```python
title = "{{BOOK_TITLE}} | Michael Rodriguez"
desc = "{{SEO_DESCRIPTION}}"
assert len(title) <= 58, f"TITLE TOO LONG: {len(title)} chars — trim it"
assert len(desc) <= 150, f"DESCRIPTION TOO LONG: {len(desc)} chars — trim it"
print(f"✅ Title: {len(title)} chars | Description: {len(desc)} chars")
```

---

## BLOCK 2 — PERFORMANCE TAGS (in `<head>`, before CSS)

```html
<link rel="preload" href="https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp" as="image" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://www.amazon.com">
<link rel="dns-prefetch" href="https://www.amazon.com">
```

---

## BLOCK 3 — CRITICAL CSS (inline, minified)

```html
<style>
.book-btn{background:#1a3c65;color:#fff;padding:10px 16px;border-radius:6px;text-decoration:none;font-weight:700;display:inline-block;text-align:center;min-width:110px;border:0}.book-btn:hover{text-decoration:none;color:#fff;opacity:0.9}.book-btn-amazon{background:#ff9900}.book-btn-apple{background:#000}.book-btn-kobo{background:#1e90ff}.book-btn-bn{background:#2e8b57}.book-btn-smash{background:#ff6347}.book-buttons{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:15px}@media (max-width:768px){.book-buttons{flex-direction:column}.book-btn{width:100%;margin-bottom:5px}}
</style>
```

---

## BLOCK 4 — OPEN GRAPH + TWITTER CARDS

Place immediately after `<style>` block, before any content:

```html
<!-- Open Graph -->
<meta property="og:type" content="book">
<meta property="og:title" content="{{BOOK_TITLE}}">
<meta property="og:description" content="{{SEO_DESCRIPTION}}">
<meta property="og:image" content="https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp">
<meta property="og:image:width" content="400">
<meta property="og:image:height" content="600">
<meta property="og:url" content="https://michaelrodriguezbooks.com/books/{{book-slug}}">
<meta property="og:site_name" content="Michael Rodriguez Books">
<meta property="book:author" content="Michael Rodriguez">
<meta property="book:isbn" content="{{ISBN_EBOOK}}">

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{BOOK_TITLE}}">
<meta name="twitter:description" content="{{SEO_DESCRIPTION}}">
<meta name="twitter:image" content="https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp">
<meta name="twitter:image:alt" content="{{BOOK_TITLE}} by Michael Rodriguez — book cover">
<meta name="twitter:creator" content="@MRodriguezBooks">
<meta name="twitter:site" content="@MRodriguezBooks">
```

> ⚠️ All URLs must be absolute (`https://...`). Relative paths break Facebook and Twitter scrapers.

---

## BLOCK 5 — JSON-LD SCHEMA (triple @graph)

Place at the bottom of the page, before `</body>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": "https://michaelrodriguezbooks.com/books/{{book-slug}}/#webpage",
      "url": "https://michaelrodriguezbooks.com/books/{{book-slug}}",
      "name": "{{BOOK_TITLE}} | Michael Rodriguez",
      "description": "{{SEO_DESCRIPTION}}",
      "datePublished": "{{YYYY-MM-DD}}",
      "dateModified": "{{YYYY-MM-DD}}",
      "inLanguage": "en",
      "isPartOf": {
        "@id": "https://michaelrodriguezbooks.com/#website"
      },
      "about": {
        "@id": "https://michaelrodriguezbooks.com/books/{{book-slug}}/#book"
      }
    },
    {
      "@type": "Book",
      "@id": "https://michaelrodriguezbooks.com/books/{{book-slug}}/#book",
      "name": "{{FULL_BOOK_TITLE_WITH_SUBTITLE}}",
      "author": {
        "@type": "Person",
        "name": "Michael Rodriguez",
        "@id": "https://michaelrodriguezbooks.com/about/#person"
      },
      "publisher": {
        "@type": "Organization",
        "name": "Resource Economics Press"
      },
      "datePublished": "{{YYYY-MM-DD}}",
      "isbn": ["{{ISBN_HARDCOVER}}", "{{ISBN_EBOOK}}"],
      "bookFormat": ["Hardcover", "EBook"],
      "inLanguage": "en",
      "genre": ["{{GENRE_1}}", "{{GENRE_2}}", "{{GENRE_3}}"],
      "description": "{{SEO_DESCRIPTION}}",
      "image": "https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp",
      "url": "https://michaelrodriguezbooks.com/books/{{book-slug}}",
      "offers": [
        {
          "@type": "Offer",
          "price": "14.99",
          "priceCurrency": "USD",
          "availability": "https://schema.org/InStock",
          "url": "{{LINK_AMAZON}}"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "@id": "https://michaelrodriguezbooks.com/books/{{book-slug}}/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "{{FAQ_Q1}}",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "{{FAQ_A1}}"
          }
        },
        {
          "@type": "Question",
          "name": "{{FAQ_Q2}}",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "{{FAQ_A2}}"
          }
        },
        {
          "@type": "Question",
          "name": "{{FAQ_Q3}}",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "{{FAQ_A3}}"
          }
        },
        {
          "@type": "Question",
          "name": "{{FAQ_Q4}}",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "{{FAQ_A4}}"
          }
        }
      ]
    }
  ]
}
</script>
```

**FAQ writing rules:**
- Q1: "What is [Book Title] about?" — general hook answer
- Q2: Core question from book's main theme
- Q3: Specific revelation or unique finding
- Q4: "Is [Book Title] based on verified evidence/research?"
- Each answer: 2–4 sentences, keyword-rich, no speculation

---

## BLOCK 6 — IMAGE TAG (mandatory attributes)

```html
<img src="https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp"
     alt="{{BOOK_TITLE}} by Michael Rodriguez — {{GENRE}} book cover"
     width="400" height="600"
     loading="lazy" decoding="async">
```

> `alt` must describe the image meaningfully — include title, author, genre. Never leave it as just the filename.

---
## VALIDATION CHECKLIST (run before git commit)

```
SEO BLOCK                    | CHECK
-----------------------------|------------------------------------------
Title length                 | ≤ 58 characters (count exactly)
Description length           | ≤ 150 characters (count exactly)
Canonical URL                | Absolute https:// URL, correct slug
og:image                     | Absolute https:// URL (not site.baseurl)
og:image dimensions          | width=400 height=600 present
Twitter Card type            | summary_large_image
JSON-LD: WebPage node        | Present with datePublished + dateModified
JSON-LD: Book node           | Both ISBNs, publisher, genre, offers
JSON-LD: FAQPage node        | 4 questions, all answers 2-4 sentences
Image alt text               | Descriptive (title + author + genre)
Preload tag                  | Absolute URL, fetchpriority="high"
```

**Test tools after publishing:**
- Google Rich Results: https://search.google.com/test/rich-results
- Facebook Debugger: https://developers.facebook.com/tools/debug/
- Twitter Card Validator: https://cards-dev.twitter.com/validator
- PageSpeed Insights: https://pagespeed.web.dev/ (target: 75+)

---

## BLOCK 7 — BLOGPOSTING SCHEMA (for blog posts only)

Use this instead of Book Schema when creating blog posts (FAQ or analytical articles):

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{{POST_TITLE}}",
  "description": "{{SEO_DESCRIPTION}}",
  "image": "https://michaelrodriguezbooks.com/assets/images/{{filename}}.webp",
  "author": {
    "@type": "Person",
    "name": "Michael Rodriguez",
    "url": "https://michaelrodriguezbooks.com/about/"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Michael Rodriguez Books",
    "url": "https://michaelrodriguezbooks.com/"
  },
  "datePublished": "{{YYYY-MM-DD}}",
  "dateModified": "{{YYYY-MM-DD}}",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://michaelrodriguezbooks.com/blog/{{slug}}/"
  },
  "url": "https://michaelrodriguezbooks.com/blog/{{slug}}/",
  "wordCount": {{WORD_COUNT}},
  "inLanguage": "en",
  "keywords": ["{{keyword1}}", "{{keyword2}}", "{{keyword3}}"]
}
</script>
```

> For **FAQ blog posts**: combine BlogPosting Schema with FAQPage Schema using `@graph` array.
> For **analytical articles**: use BlogPosting Schema only.

---

## BLOCK 8 — KIT NEWSLETTER FORM (embed on every page)

Place in the "Subscribe to Newsletter" section at the bottom of every page:

```html
<h2>Subscribe to Newsletter</h2>
<p>Get updates on new books, exclusive content, and free chapters from Michael Rodriguez.</p>
<script async data-uid="b2a1614bc4" src="https://michael-rodriguez.kit.com/b2a1614bc4/index.js"></script>
```

> Kit form ID: `b2a1614bc4` — same for all pages across the site.

---

## BLOCK 9 — RELATED ARTICLES & RELATED BOOKS (cross-linking)

Every blog post MUST include both Related sections at the bottom (before Newsletter):

### Related Articles:
```html
<h3>📚 Related Articles</h3>
<ul>
  <li><a href="{{ site.baseurl }}/blog/{{related-slug-1}}">{{Related Article Title 1}}</a></li>
  <li><a href="{{ site.baseurl }}/blog/{{related-slug-2}}">{{Related Article Title 2}}</a></li>
  <li><a href="{{ site.baseurl }}/blog/{{related-slug-3}}">{{Related Article Title 3}}</a></li>
</ul>
```

### Related Books:
```html
<h3>📕 Related Books</h3>
<ul>
  <li><a href="{{ site.baseurl }}/books/{{related-book-slug-1}}">{{Related Book Title 1}}</a></li>
  <li><a href="{{ site.baseurl }}/books/{{related-book-slug-2}}">{{Related Book Title 2}}</a></li>
</ul>
```

**Selection rules:**
- Choose articles on **thematically adjacent** topics (e.g., politics → economics → corruption)
- Choose books in **adjacent genres** from the catalog
- Minimum 2, maximum 4 links per section
- Cross-link bidirectionally: when adding Related Articles to a new post, also update existing posts to link back

---

## BLOCK 10 — CTA BOX WITH DUAL BUTTONS (for blog posts)

Every blog post should have a CTA box with **two** buttons — Amazon direct purchase + Free Chapter lead magnet:

```html
<div class="cta-box" style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 30px; border-radius: 12px; margin: 30px 0; border: 2px solid #c9a227; text-align: center;">
  <h3 style="color: #c9a227; margin-top: 0;">📖 Get the Full Story</h3>
  <p style="color: #ccc;">Discover the complete investigation in <strong>{{BOOK_TITLE}}</strong></p>
  <a href="{{AMAZON_DIRECT_LINK}}" class="btn-amazon" style="background: #ff9900; color: #fff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 700; margin: 5px;">📦 Buy on Amazon</a>
  <a href="{{ site.baseurl }}/books/free-chapter-{{book-slug}}" class="btn-free" style="background: #2e8b57; color: #fff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 700; margin: 5px;">📖 Read Free Chapter</a>
</div>
```

---

## BLOCK 11 — FREE CHAPTER BANNER (for book pages)

Insert on every book page BEFORE "About the Book" section:

```html
<div style="background: linear-gradient(135deg, #1a3c65 0%, #0d253f 100%); padding: 20px 25px; border-radius: 10px; margin: 20px 0; border: 1px solid #c9a227; text-align: center;">
  <a href="{{ site.baseurl }}/books/free-chapter-{{book-slug}}" style="color: #c9a227; font-size: 1.2rem; font-weight: 700; text-decoration: none;">📖 Read First 2 Chapters FREE →</a>
</div>
```

> This banner links to the Free Chapter lead magnet page where visitors can read preview chapters and subscribe via Kit form.