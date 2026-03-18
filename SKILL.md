# SKILL: Draft2Digital Book Publisher
**Role:** Professional Digital Publishing Engineer  
**Mission:** Convert `Full_Book.md` into a clean, professionally styled, Draft2Digital-ready Word document.  
**Output:** `Final_Book.docx`

---

## IMPORTANT: FILE PATHS

All file paths in this skill refer to the **book project's output directory**:
```
/Users/zews/Book/[Book_Name]/output/
```

When this skill mentions `Full_Book.md`, it means:
```
/Users/zews/Book/[Book_Name]/output/Full_Book.md
```

The working directory for all commands should be the book's output folder.

---

## KEY PRINCIPLE: PANDOC + PYTHON-DOCX PIPELINE

Pandoc converts Markdown → DOCX, but its output needs post-processing:
- Pandoc **ignores** all inline CSS (`style="text-align: center"`, `font-size`, etc.)
- Pandoc uses **Aptos** as default font (not professional for books)
- Pandoc does **not** insert page breaks between front matter sections
- D2D does **not** automatically separate title, copyright, and about pages

**The pipeline is always:**
1. Build clean Markdown with YAML front matter
2. Convert with Pandoc → raw DOCX
3. Post-process with python-docx → styled DOCX with page breaks, fonts, alignment

Never skip step 3. The raw Pandoc output is NOT ready for D2D.

---

## PRE-FLIGHT: READ THE SOURCE FILE FIRST

```bash
wc -w Full_Book.md          # Approximate word count
head -100 Full_Book.md      # Inspect structure
grep -n "^#" Full_Book.md   # List all headings
```

Check:
- Does the file exist and is it UTF-8 encoded?
- What heading structure is already in use (H1/H2/H3)?
- Are there Parts, Chapters, or only Chapters?
- Are there images? (If yes — note them, D2D handles images separately)
- Approximate word count (minimum target: 30,000 words)

If word count is below 30,000 — **stop and report** to the user before continuing.

---

## STAGE 1 — NORMALIZE HEADING HIERARCHY

D2D detects structure through Word heading styles, which Pandoc maps from Markdown.  
Use this exact hierarchy:

| Element       | Markdown  | Maps to Word Style |
|--------------|-----------|-------------------|
| Book title   | YAML only | Title             |
| Subtitle     | YAML only | Subtitle          |
| Author       | YAML only | Author            |
| Part title   | `# Part`  | Heading 1         |
| Chapter title| `## Ch`   | Heading 2         |
| Subsection   | `### Sub` | Heading 3         |
| Body text    | plain     | Normal / Body Text|

> ⚠️ **Do NOT put the book title as `#` in the body.** It goes in YAML front matter only.  
> ⚠️ **Do NOT use `#` for anything except Part titles.**

**Cleaning rules — apply all:**
- Remove manual line breaks (`\` at end of line)
- Collapse 3+ consecutive blank lines → single blank line
- Remove tabs → replace with space
- Remove double spaces
- Remove decorative separators: `---`, `***`, `* * *`, `===` (except YAML delimiters)
- Remove `<br>`, `<center>`, `<div>`, and all raw HTML tags (they are ignored by Pandoc DOCX anyway)
- Remove inline CSS — `style="..."` attributes have zero effect on DOCX output
- Remove forced page break commands: `\newpage`, `\pagebreak`

Run the cleanup as a Python script to ensure consistency:

```python
import re

text = open("Full_Book.md", encoding="utf-8").read()

# Remove decorative separators (but preserve YAML --- at top)
lines = text.split("\n")
clean_lines = []
in_yaml = False
for i, line in enumerate(lines):
    if i == 0 and line.strip() == "---":
        in_yaml = True
        clean_lines.append(line)
        continue
    if in_yaml and line.strip() == "---":
        in_yaml = False
        clean_lines.append(line)
        continue
    if not in_yaml and re.match(r"^[-*=]{3,}\s*$", line):
        continue  # Skip decorative separators
    clean_lines.append(line)

text = "\n".join(clean_lines)

# Remove manual line breaks
text = re.sub(r"\\\n", " ", text)
# Collapse multiple blank lines
text = re.sub(r"\n{3,}", "\n\n", text)
# Remove tabs
text = text.replace("\t", " ")
# Remove double spaces
text = re.sub(r"  +", " ", text)
# Remove raw HTML (div, center, br, span, style attributes, etc.)
text = re.sub(r"<[^>]+>", "", text)

open("Full_Book_clean.md", "w", encoding="utf-8").write(text)
print("Done. Lines:", text.count("\n"))
```

---

## STAGE 2 — ADD YAML FRONT MATTER + FRONT MATTER PAGES

### 2a. YAML front matter (document metadata)

Add this **at the very top** of `Full_Book_clean.md`:

```yaml
---
title: "Your Book Title"
subtitle: "Subtitle if exists"
author: "Author Name"
rights: "© 2026 Author Name. All rights reserved."
lang: "en"
---
```

> For Russian-language books use `lang: "ru"`.  
> Do not add any other fields — keep it minimal.  
> Pandoc maps these to Word's Title, Subtitle, and Author styles automatically.

### 2b. COPYRIGHT PAGE (visible to readers)

Immediately after the closing `---` of YAML, add the copyright page as plain paragraphs.  
**No Markdown headings. No bold. No HTML.** Just plain text with blank lines between blocks:

```
COPYRIGHT PAGE

© 2026 Author Name. All rights reserved.

The moral right of the author has been asserted. No part of this book may be reproduced,
stored in a retrieval system, or transmitted in any form or by any means electronic,
mechanical, photocopying, recording, or otherwise without prior written permission
from the publisher.

This book contains the author's opinions and analysis of [TOPIC] up to [DATE]. It is
sold with the understanding that the author is not engaged in rendering professional
financial or investment advice.

First edition: [Month Year]

Published by [Publisher Name]

[City] · [City] · [City]
```

**Copyright page styling (applied in Stage 4 post-processing):**
- Font: Garamond, 10pt
- Alignment: centered
- Page break inserted AFTER this section

### 2c. ABOUT THE AUTHOR PAGE

After the copyright page, add an About the Author section using a Heading 2:

```
## About the Author

[Author bio text — plain paragraphs, 3-5 paragraphs. Include previous works in italics.
Mention areas of expertise, previous book titles, and credentials.
Do NOT include links to websites — publishing platforms add their own.]
```

**About the Author styling (applied in Stage 4 post-processing):**
- Font: Garamond, 12pt (same as body)
- Alignment: centered
- Page break inserted AFTER this section

### 2d. INTRODUCTION (if applicable)

After About the Author, add the Introduction as a standalone section before Part 1:

```
## INTRODUCTION

[Introduction text...]

# Part 1 of N: [Part Title]

**Summary:** [Part summary...]

## Chapter 1: [Title]
```

> ⚠️ **INTRODUCTION goes before Part 1**, not inside it.

### 2e. P.S. / CALL TO ACTION (end of book)

At the very end of the book, after the last Part, add a casual call to action:

```
## P.S. — A Word from the Author

[2-3 paragraphs. Thank the reader. Ask for a review (not pushy).
Suggest sharing the book with someone who'd enjoy it.
Do NOT include links to websites or social media — platforms handle this.]

— Author Name
```

> ⚠️ Do NOT include website links in the book body. Publishing platforms (Amazon, D2D) insert their own author pages and links. External URLs can trigger review flags.

---

## STAGE 3 — CONVERT WITH PANDOC

### Prerequisites

```bash
pandoc --version   # Must be 2.11 or higher
pip install python-docx  # Required for Stage 4
```

### Conversion command

```bash
pandoc Full_Book_clean.md \
  --from markdown+smart \
  --to docx \
  --output Final_Book.docx
```

**Flags explained:**
- `+smart` — converts `--` to em-dashes, `"quotes"` to curly quotes automatically
- No `--reference-doc` — keep default Word styles (post-processing handles fonts)
- No `--toc` — D2D generates its own TOC
- No `--number-sections` — no auto-numbering

---

## STAGE 4 — POST-PROCESS WITH PYTHON-DOCX (CRITICAL)

This is the most important step. Pandoc output uses Aptos font and has no page breaks between front matter sections. This script fixes everything:

```python
"""
Post-process Final_Book.docx for Draft2Digital:
1. Set Garamond as default font (12pt body text)
2. Copyright page: Garamond 10pt, centered
3. About the Author: Garamond 12pt, centered
4. Subtitle: 20pt
5. Page breaks between: Title → Copyright → About → Introduction
"""
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def add_page_break_after(paragraph):
    """Insert a page break at the end of a paragraph."""
    run = paragraph.add_run()
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    run._element.append(br)


doc = Document("Final_Book.docx")

# --- STEP 1: Identify key sections by paragraph index ---
title_idx = None
subtitle_idx = None
author_idx = None
copyright_start = None
copyright_end = None
about_heading_idx = None
about_end_idx = None
intro_idx = None

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    style = p.style.name

    if style == "Title":
        title_idx = i
    elif style == "Subtitle":
        subtitle_idx = i
    elif style == "Author":
        author_idx = i
    elif text == "COPYRIGHT PAGE" and copyright_start is None:
        copyright_start = i
    elif text == "About the Author" and style.startswith("Heading"):
        about_heading_idx = i
        # Copyright ends just before About heading
        copyright_end = i - 1
        while copyright_end > (copyright_start or 0) and not doc.paragraphs[copyright_end].text.strip():
            copyright_end -= 1
    elif text == "INTRODUCTION" and style.startswith("Heading"):
        intro_idx = i
        # About section ends just before Introduction
        about_end_idx = i - 1
        while about_end_idx > (about_heading_idx or 0) and not doc.paragraphs[about_end_idx].text.strip():
            about_end_idx -= 1
        break

print(f"Title: {title_idx}, Subtitle: {subtitle_idx}, Author: {author_idx}")
print(f"Copyright: {copyright_start}-{copyright_end}")
print(f"About: {about_heading_idx}-{about_end_idx}")
print(f"Intro: {intro_idx}")

# --- STEP 2: Apply fonts and styling ---
in_copyright = False
in_about = False

for i, para in enumerate(doc.paragraphs):
    style = para.style.name

    # Track sections
    if i == copyright_start:
        in_copyright = True
    if i == about_heading_idx:
        in_copyright = False
        in_about = True
    if i == intro_idx:
        in_about = False

    # Set Garamond on ALL runs
    for run in para.runs:
        run.font.name = "Garamond"

    # Title page: centered
    if style in ("Title", "Author"):
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtitle: centered, 20pt
    if style == "Subtitle":
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.font.size = Pt(20)

    # Copyright section: 10pt, centered
    elif in_copyright:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.font.size = Pt(10)

    # About the Author: 12pt, centered
    elif in_about:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.font.size = Pt(12)

    # Normal body text: 12pt
    elif not style.startswith("Heading") and style not in ("Title", "Subtitle", "Author"):
        for run in para.runs:
            run.font.size = Pt(12)

# --- STEP 3: Insert page breaks ---
if author_idx is not None:
    add_page_break_after(doc.paragraphs[author_idx])
    print(f"Page break after Title page (idx {author_idx})")

if copyright_end is not None:
    add_page_break_after(doc.paragraphs[copyright_end])
    print(f"Page break after Copyright (idx {copyright_end})")

if about_end_idx is not None:
    add_page_break_after(doc.paragraphs[about_end_idx])
    print(f"Page break after About the Author (idx {about_end_idx})")

# --- STEP 4: Set default document style ---
ns = doc.styles["Normal"]
ns.font.name = "Garamond"
ns.font.size = Pt(12)

doc.save("Final_Book.docx")
print("Done. Professional styling applied.")
```

**What this script does:**
- **Garamond** as the primary font (professional book standard)
- **Title page** (Title + Subtitle + Author) → own page, centered
- **Copyright page** → own page, 10pt, centered
- **About the Author** → own page, 12pt, centered
- **Page breaks** between each front matter section
- **Subtitle** at 20pt for visual hierarchy
- **Body text** at 12pt throughout

> ⚠️ **This post-processing step is NOT optional.** Without it, D2D will render all front matter on a single page with the wrong font.

---

## STAGE 5 — AUTOMATED VALIDATION

Run this validation script after post-processing:

```python
from docx import Document
from docx.oxml.ns import qn
import re

doc = Document("Final_Book.docx")

word_count = sum(len(p.text.split()) for p in doc.paragraphs if p.text.strip())
h1 = [p.text for p in doc.paragraphs if p.style.name == "Heading 1"]
h2 = [p.text for p in doc.paragraphs if p.style.name == "Heading 2"]
h3 = [p.text for p in doc.paragraphs if p.style.name == "Heading 3"]

# Check for leftover Markdown artifacts
artifacts = [p.text for p in doc.paragraphs if re.search(r"^#{1,6} |^---$", p.text)]

# Check copyright page
copyright_present = any("©" in p.text or "COPYRIGHT PAGE" in p.text for p in doc.paragraphs)

# Check About the Author
about_present = any("About the Author" in p.text for p in doc.paragraphs)

# Check font
default_font = doc.styles["Normal"].font.name

# Count page breaks
page_breaks = 0
for p in doc.paragraphs:
    for run in p.runs:
        for br in run._element.findall(qn("w:br")):
            if br.get(qn("w:type")) == "page":
                page_breaks += 1

# Check for external links in body
links_found = []
for p in doc.paragraphs:
    if "http" in p.text.lower() or ".com" in p.text.lower():
        if not p.style.name.startswith("Heading"):
            links_found.append(p.text[:60])

print(f"Word count    : {word_count:,}")
print(f"Parts (H1)    : {len(h1)}")
print(f"Chapters (H2) : {len(h2)}")
print(f"Sections (H3) : {len(h3)}")
print(f"Default font  : {default_font}")
print(f"Page breaks   : {page_breaks}")
print()

checks = []
checks.append(("Word count >= 30,000", word_count >= 30000))
checks.append(("Headings detected", bool(h1 or h2)))
checks.append(("No Markdown artifacts", len(artifacts) == 0))
checks.append(("Copyright page present", copyright_present))
checks.append(("About the Author present", about_present))
checks.append(("Garamond font set", default_font == "Garamond"))
checks.append(("Page breaks >= 3 (title/copyright/about)", page_breaks >= 3))
checks.append(("No external links in body", len(links_found) == 0))

all_pass = True
for name, passed in checks:
    icon = "PASS" if passed else "FAIL"
    print(f" [{icon}] {name}")
    if not passed:
        all_pass = False

print()
if all_pass:
    print("STATUS: READY FOR D2D")
else:
    print("STATUS: NEEDS FIX")

if artifacts:
    print(f"\nArtifacts found ({len(artifacts)}):")
    for a in artifacts[:5]:
        print(f"  -> {a[:80]}")

if links_found:
    print(f"\nExternal links found ({len(links_found)}):")
    for l in links_found[:5]:
        print(f"  -> {l}")
```

**Validation pass criteria:**
- Word count ≥ 30,000
- Headings present (H1 Parts + H2 Chapters)
- Zero Markdown artifacts
- Copyright page present
- About the Author present
- Garamond font set as default
- At least 3 page breaks (title → copyright → about → body)
- No external links in body text

---

## STAGE 6 — D2D STRUCTURE CHECKLIST

Before uploading to Draft2Digital, confirm:

- [ ] File is `.docx` (not `.doc`)
- [ ] Parts appear as **Heading 1** in Word's Navigation Pane
- [ ] Chapters appear as **Heading 2** in Word's Navigation Pane
- [ ] No visible `#`, `*`, `---` symbols anywhere in text
- [ ] **Title page** is a separate page (Title + Subtitle + Author)
- [ ] **Copyright page** is a separate page (smaller font, centered)
- [ ] **About the Author** is a separate page (centered)
- [ ] **Introduction** starts on its own page after About the Author
- [ ] © symbol and publisher info present and correct
- [ ] Font is Garamond throughout
- [ ] No external URLs in the book body
- [ ] File size is reasonable (under 50MB)
- [ ] No password protection on the file

---

## DOCUMENT PAGE STRUCTURE (D2D expected order)

```
Page 1:  TITLE PAGE          <- Title (large), Subtitle (20pt), Author
         ---- page break ----
Page 2:  COPYRIGHT PAGE      <- 10pt, centered, all rights reserved
         ---- page break ----
Page 3:  ABOUT THE AUTHOR    <- 12pt, centered, bio + previous works
         ---- page break ----
Page 4:  INTRODUCTION        <- Normal body text begins
         ...
Page N:  BODY (Parts/Chapters)
         ...
Last:    P.S. — A Word from the Author  <- Call to action for reviews
```

---

## OUTPUT DELIVERABLES

Provide all three:

1. **`Full_Book_clean.md`** — cleaned source with YAML front matter, copyright, about, and P.S.
2. **`Final_Book.docx`** — Post-processed Word file (Garamond, page breaks, styled)
3. **Validation Report** in this format:

```
=== VALIDATION REPORT ===
Word count     : XX,XXX
Parts (H1)     : X
Chapters (H2)  : XX
Sections (H3)  : X
Default font   : Garamond
Page breaks    : X
Copyright page : Present / Missing
About Author   : Present / Missing
External links : None / [list issues]
Status         : READY FOR D2D / NEEDS FIX
```

---

## COMMON PITFALLS (LESSONS LEARNED)

| Pitfall | Why it happens | Solution |
|---------|---------------|----------|
| All front matter on one page | Pandoc does not insert page breaks | Post-process with python-docx (Stage 4) |
| Aptos font in output | Pandoc uses system default | Set Garamond via python-docx |
| CSS styling ignored | Pandoc DOCX ignores `style="..."` | Never use inline CSS in MD for DOCX |
| `<div>`, `<center>` ignored | Pandoc strips HTML for DOCX | Use python-docx for alignment |
| External links flagged | Amazon/D2D may reject or flag | Remove all URLs from body text |
| Wrong font size on subtitle | Pandoc uses default heading size | Set 20pt via python-docx |
| About the Author missing | Not in standard Pandoc output | Add as `## About the Author` in MD |
| No call to action | Lost opportunity for reviews | Add P.S. section at end of book |
| Inline Python garbled in zsh | Quotes conflict with shell | Always use separate .py files |
