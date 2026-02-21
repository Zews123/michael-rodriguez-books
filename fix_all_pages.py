#!/usr/bin/env python3
"""Batch fix: FA icons → SVG, aria-labels, dark CSS, @import removal, newsletter dark."""
import re
import os
import glob

REPO = "/Users/zews/Book/michael-rodriguez-books"

# ─── SVG icons ───
SVG = {
    "twitter": '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22.46 6c-.77.35-1.6.58-2.46.69a4.3 4.3 0 0 0 1.88-2.38 8.59 8.59 0 0 1-2.72 1.04 4.28 4.28 0 0 0-7.32 3.91A12.16 12.16 0 0 1 3 4.79a4.28 4.28 0 0 0 1.32 5.72 4.24 4.24 0 0 1-1.94-.54v.05a4.28 4.28 0 0 0 3.43 4.2 4.27 4.27 0 0 1-1.93.07 4.29 4.29 0 0 0 4 2.97A8.59 8.59 0 0 1 2 19.54a12.13 12.13 0 0 0 6.56 1.92c7.88 0 12.2-6.53 12.2-12.2l-.01-.56A8.72 8.72 0 0 0 23 6.29a8.49 8.49 0 0 1-.54.21z"/></svg>',
    "facebook": '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.99 3.66 9.12 8.44 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99C18.34 21.12 22 16.99 22 12z"/></svg>',
    "linkedin": '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>',
    "reddit": '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14.5 15.41c.08.08.08.22 0 .3-.65.65-1.89.7-2.5.7s-1.85-.05-2.5-.7a.21.21 0 0 1 0-.3.21.21 0 0 1 .3 0c.39.39 1.22.53 2.2.53s1.81-.14 2.2-.53a.21.21 0 0 1 .3 0zM9.74 13c0-.55.45-1 1-1s1 .45 1 1-.45 1-1 1-1-.45-1-1zm4.52-1c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zM22 12c0 5.52-4.48 10-10 10S2 17.52 2 12 6.48 2 12 2s10 4.48 10 10zm-3.87-1.14c-.55 0-1.05.24-1.41.6-.98-.54-2.24-.87-3.62-.93l.87-2.79 2.04.47c0 .55.45 1 1 1s1-.45 1-1-.45-1-1-1c-.38 0-.71.22-.87.54l-2.33-.54a.22.22 0 0 0-.26.15l-.98 3.15c-1.44.05-2.75.38-3.76.93a2 2 0 0 0-1.41-.6 2 2 0 0 0-2 2c0 .77.44 1.44 1.09 1.76-.03.22-.05.44-.05.67 0 2.65 3.14 4.8 7.01 4.8s7.01-2.15 7.01-4.8c0-.23-.02-.45-.06-.67.64-.32 1.08-.99 1.08-1.76a2 2 0 0 0-1.35-1.89z"/></svg>',
    "pinterest": '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9.04 21.54c.96.29 1.93.46 2.96.46a10 10 0 0 0 10-10A10 10 0 0 0 12 2 10 10 0 0 0 2 12c0 4.25 2.67 7.9 6.44 9.34-.09-.78-.18-2.07.04-2.96.2-.81 1.28-5.43 1.28-5.43s-.33-.65-.33-1.62c0-1.52.88-2.65 1.98-2.65.93 0 1.38.7 1.38 1.54 0 .94-.6 2.35-.91 3.65-.26 1.1.55 1.99 1.63 1.99 1.96 0 3.47-2.07 3.47-5.05 0-2.64-1.9-4.49-4.61-4.49-3.14 0-4.99 2.36-4.99 4.8 0 .95.37 1.97.82 2.52a.33.33 0 0 1 .08.32c-.08.35-.28 1.1-.32 1.25-.05.2-.16.24-.37.15-1.38-.64-2.24-2.66-2.24-4.29 0-3.47 2.52-6.65 7.28-6.65 3.83 0 6.8 2.73 6.8 6.38 0 3.8-2.39 6.86-5.72 6.86-1.12 0-2.17-.58-2.52-1.27l-.69 2.61z"/></svg>',
    "envelope": '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>',
    "hackernews": '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M2 2h20v20H2V2zm10 9.5L7.5 4H9.9l3.15 5.55h.05L16.1 4h2.4l-4.5 7.5V18h-2V11.5z"/></svg>',
}

# ─── FA icon → SVG replacement ───
FA_MAP = {
    '<i class="fab fa-twitter-square"></i>': SVG["twitter"],
    '<i class="fab fa-facebook-square"></i>': SVG["facebook"],
    '<i class="fab fa-linkedin"></i>': SVG["linkedin"],
    '<i class="fab fa-reddit-square"></i>': SVG["reddit"],
    '<i class="fab fa-pinterest-square"></i>': SVG["pinterest"],
    '<i class="fas fa-envelope-square"></i>': SVG["envelope"],
    '<i class="fab fa-hacker-news-square"></i>': SVG["hackernews"],
}

# ─── Aria-label patterns (add only if not already present) ───
ARIA_LABELS = [
    (r'twitter\.com/intent/tweet', 'Share on Twitter'),
    (r'facebook\.com/sharer', 'Share on Facebook'),
    (r'linkedin\.com/shareArticle', 'Share on LinkedIn'),
    (r'reddit\.com/submit', 'Share on Reddit'),
    (r'pinterest\.com/pin', 'Share on Pinterest'),
    (r'news\.ycombinator\.com/submitlink', 'Share on Hacker News'),
    (r'mailto:\?subject=', 'Share via Email'),
]

# ─── All light-theme accent colors → gold ───
ACCENT_COLORS_TO_GOLD = ['#1a3c65', '#e74c3c', '#8b4513']

# ─── Light body/text colors to replace ───
LIGHT_TO_DARK_COLORS = {
    'color: #333':       'color: #e8e6e3',
    'color:#333':        'color:#e8e6e3',
    'color: #555':       'color: #a0a0a0',
    'color:#555':        'color:#a0a0a0',
    'color: #777':       'color: #999',
    'color:#777':        'color:#999',
    'color: #2a6496':    'color: #c9a227',
    'color:#2a6496':     'color:#c9a227',
    'background-color: #f9f9f9': 'background-color: #1a1a1a',
    'background-color:#f9f9f9':  'background-color:#1a1a1a',
    'background-color: #f8f9fa': 'background-color: #1a1a1a',
    'background-color:#f8f9fa':  'background-color:#1a1a1a',
    'background-color: #f9f9fb': 'background-color: #1a1a1a',
    'background-color:#f9f9fb':  'background-color:#1a1a1a',
    'border: 1px solid #ddd':    'border: 1px solid #2a2a2a',
    'border:1px solid #ddd':     'border:1px solid #2a2a2a',
}


def add_aria_labels(content):
    """Add aria-labels to social share links if missing."""
    changed = False
    for url_pattern, label in ARIA_LABELS:
        # Find links matching the URL pattern that don't have aria-label
        def add_label(m):
            tag = m.group(0)
            if 'aria-label=' in tag:
                return tag
            return tag[:-1] + f' aria-label="{label}">'
        
        new_content = re.sub(
            r'<a\s+[^>]*href="[^"]*' + url_pattern + r'[^"]*"[^>]*>',
            add_label,
            content
        )
        if new_content != content:
            content = new_content
            changed = True
    return content, changed


def remove_share_inline_colors(content):
    """Remove inline style='color:#...' from social share links."""
    # Match social share link inline color styles
    patterns = [
        (r'(style="[^"]*?)color:\s*#[0-9a-fA-F]+;\s*', r'\1'),
        # For style that is ONLY color
    ]
    
    # More targeted: remove just the color from style attrs on social share links
    def clean_share_style(m):
        full = m.group(0)
        # Remove color:#xxx from style, preserving other style properties
        cleaned = re.sub(r'\bcolor:\s*#[0-9a-fA-F]+;?\s*', '', full)
        # If style is now empty, remove the whole style attr
        cleaned = re.sub(r'\s*style="\s*"', '', cleaned)
        # Also clean display/margin/font-size since layout handles these
        cleaned = re.sub(r'\s*style="display:\s*inline-block;\s*margin-right:\s*\d+px;\s*font-size:\s*\d+px;\s*"', '', cleaned)
        cleaned = re.sub(r'\s*style="display:\s*inline-block;\s*margin-right:\s*\d+px;\s*font-size:\s*\d+px;\s*color:\s*#[0-9a-fA-F]+;\s*"', '', cleaned)
        return cleaned
    
    # Target social share links specifically
    social_urls = [
        r'twitter\.com/intent/tweet',
        r'facebook\.com/sharer',
        r'linkedin\.com/shareArticle',
        r'reddit\.com/submit',
        r'pinterest\.com/pin',
        r'news\.ycombinator\.com/submitlink',
        r'mailto:\?subject=',
    ]
    
    for url_pat in social_urls:
        content = re.sub(
            r'<a\s+[^>]*href="[^"]*' + url_pat + r'[^"]*"[^>]*>',
            clean_share_style,
            content
        )
    
    return content


def fix_blog_inline_css(content):
    """Replace entire inline <style> blocks in blog posts with dark theme versions."""
    changed = False
    
    # Pattern: match <style>...</style> blocks containing light-theme body color
    # This catches both English and Russian comment variations
    style_blocks = list(re.finditer(r'<style>(.*?)</style>', content, re.DOTALL))
    
    if not style_blocks:
        return content, False
    
    # Process style blocks in reverse order to preserve positions
    for block in reversed(style_blocks):
        css_text = block.group(1)
        
        # Identify if this is a "critical" style block (has body { ... color: #333 })
        if re.search(r'body\s*\{[^}]*color:\s*#333', css_text):
            # This is the critical CSS — replace with dark version
            dark_css = css_text
            
            # Replace body text color
            dark_css = re.sub(r'(body\s*\{[^}]*?)color:\s*#333', r'\1color: #e8e6e3', dark_css)
            
            # Replace font-family in body
            dark_css = re.sub(
                r'(body\s*\{[^}]*?)font-family:\s*"Times New Roman"[^;]*;',
                r'\1font-family: Georgia, "Times New Roman", serif;',
                dark_css
            )
            dark_css = re.sub(r'(body\s*\{[^}]*?)line-height:\s*1\.6', r'\1line-height: 1.75', dark_css)
            
            # Replace heading colors (all accent variants)
            for accent in ACCENT_COLORS_TO_GOLD:
                dark_css = dark_css.replace(f'color: {accent}', 'color: #c9a227')
                dark_css = dark_css.replace(f'color:{accent}', 'color:#c9a227')
                dark_css = dark_css.replace(f'border-bottom: 2px solid {accent}', 'border-bottom: 1px solid #2a2a2a')
                dark_css = dark_css.replace(f'border-left: 4px solid {accent}', 'border-left: 4px solid #c9a227')
                dark_css = dark_css.replace(f'border-left: 3px solid {accent}', 'border-left: 3px solid #c9a227')
            
            # Replace link color
            dark_css = dark_css.replace('color: #2a6496', 'color: #c9a227')
            dark_css = dark_css.replace('color:#2a6496', 'color:#c9a227')
            
            # Replace date color
            dark_css = dark_css.replace('color: #777', 'color: #999')
            
            # Replace blockquote (if in critical block)
            dark_css = dark_css.replace('color: #555', 'color: #a0a0a0')
            dark_css = dark_css.replace('background-color: #f9f9f9', 'background-color: #1a1a1a')
            
            # If border-bottom is 1px dotted, make it transparent
            dark_css = dark_css.replace('border-bottom: 1px dotted', 'border-bottom: 1px solid transparent')
            
            # Replace hover colors to gold
            dark_css = re.sub(r'a:hover\s*\{[^}]*?color:\s*#[0-9a-fA-F]+', 
                            lambda m: m.group(0).replace(m.group(0).split('color:')[-1].strip(), ' #e8d48b'), 
                            dark_css)
            # Simpler hover fix
            for accent in ACCENT_COLORS_TO_GOLD:
                dark_css = dark_css.replace(f'color: {accent}', 'color: #c9a227')
            
            # Add gradient to h1 if not present
            if 'background-clip' not in dark_css and 'h1 {' in dark_css:
                dark_css = re.sub(
                    r'(h1\s*\{[^}]*)(})',
                    r'\1  background: linear-gradient(135deg, #c9a227 0%, #e8d48b 100%);\n  -webkit-background-clip: text;\n  -webkit-text-fill-color: transparent;\n  background-clip: text;\n\2',
                    dark_css
                )
            
            content = content[:block.start()] + f'<style>{dark_css}</style>' + content[block.end():]
            changed = True
        
        # Identify non-critical style blocks (responsive + social share at bottom)
        elif re.search(r'@media\s*\(max-width', css_text) and 'book-container' in css_text:
            # Non-critical responsive CSS — update colors
            dark_css = css_text
            for accent in ACCENT_COLORS_TO_GOLD:
                dark_css = dark_css.replace(f'color: {accent}', 'color: #c9a227')
                dark_css = dark_css.replace(f'color:{accent}', 'color:#c9a227')
            
            content = content[:block.start()] + f'<style>{dark_css}</style>' + content[block.end():]
            changed = True
        
        # Catch any standalone blockquote style blocks
        elif re.search(r'blockquote\s*\{', css_text) and 'color: #555' in css_text:
            dark_css = css_text
            dark_css = dark_css.replace('color: #555', 'color: #a0a0a0')
            dark_css = dark_css.replace('background-color: #f9f9f9', 'background-color: #1a1a1a')
            for accent in ACCENT_COLORS_TO_GOLD:
                dark_css = dark_css.replace(f'border-left: 3px solid {accent}', 'border-left: 3px solid #c9a227')
            
            # Remove @import Google Fonts
            dark_css = re.sub(r"@import url\(['\"]?https://fonts\.googleapis\.com[^)]*\)['\"]?;\s*\n?", '', dark_css)
            
            content = content[:block.start()] + f'<style>{dark_css}</style>' + content[block.end():]
            changed = True
    
    return content, changed


def fix_inline_style_colors(content):
    """Fix inline style= light colors in HTML elements (newsletter, cards, etc.)."""
    changed = False
    original = content
    
    for old, new in LIGHT_TO_DARK_COLORS.items():
        content = content.replace(old, new)
    
    # Fix accent colors in inline styles
    for accent in ACCENT_COLORS_TO_GOLD:
        # color: #accent → color: #c9a227
        content = content.replace(f'color: {accent}', 'color: #c9a227')
        content = content.replace(f'color:{accent}', 'color:#c9a227')
        # background: #accent → background: #c9a227 (for buttons, keep them)
        content = content.replace(f'background:{accent}', 'background:#c9a227')
        content = content.replace(f'background: {accent}', 'background: #c9a227')
    
    # Fix newsletter info text color
    content = content.replace('color: #666', 'color: #999')
    content = content.replace('color:#666', 'color:#999')
    
    if content != original:
        changed = True
    
    return content, changed


def fix_file(filepath):
    """Apply all fixes to a single file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    changes = []
    is_blog = filepath.endswith('.html') and '/blog/' in filepath
    is_book = '/books/' in filepath and filepath.endswith('.md')
    
    # 1. Replace FA icons with SVG
    for fa, svg in FA_MAP.items():
        if fa in content:
            content = content.replace(fa, svg)
            changes.append("FA→SVG")
    
    # 2. Add aria-labels to social share links
    content, aria_changed = add_aria_labels(content)
    if aria_changed:
        changes.append("aria-label")
    
    # 3. Remove @import url(Google Fonts) 
    import_pattern = r"@import url\(['\"]?https://fonts\.googleapis\.com[^)]*\)['\"]?;\s*\n?"
    new_content = re.sub(import_pattern, '', content)
    if new_content != content:
        content = new_content
        changes.append("rm @import")
    
    # 4. Remove inline color styles from social share links
    new_content = remove_share_inline_colors(content)
    if new_content != content:
        content = new_content
        changes.append("rm share colors")
    
    # 5. Fix blog inline CSS (light → dark theme)
    if is_blog:
        content, css_changed = fix_blog_inline_css(content)
        if css_changed:
            changes.append("dark CSS")
    
    # 6. Fix inline style colors on HTML elements (newsletters, cards, etc.)
    content, style_changed = fix_inline_style_colors(content)
    if style_changed:
        changes.append("dark inline")
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True, list(set(changes))
    return False, []


def fix_blog_card_page(filepath):
    """Fix blog.md card page colors for dark theme."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Update blog card CSS colors
    replacements = {
        'color: #0f2c4c': 'color: #c9a227',
        'color:#0f2c4c': 'color:#c9a227',
        'color: #2c2c2c': 'color: #999',
        'color:#2c2c2c': 'color:#999',
        'background-color: #0f2c4c': 'background-color: #c9a227',
        'background-color:#0f2c4c': 'background-color:#c9a227',
        'background-color: #d73527': 'background-color: #c9a227',
        'border-color: #d73527': 'border-color: #c9a227',
        'background-color: #fff': 'background-color: #1a1a1a',
        'background-color:#fff': 'background-color:#1a1a1a',
        'outline: 3px solid #ffbf00': 'outline: 3px solid #c9a227',
        'color: white': 'color: #0d0d0d',
        'box-shadow: 0 2px 8px rgba(0,0,0,0.08)': 'box-shadow: 0 2px 8px rgba(0,0,0,0.3)',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False


def main():
    skip = {"Shadows_of_Power.md"}  # Already optimized
    
    all_files = []
    
    # Collect all files
    book_files = sorted(glob.glob(os.path.join(REPO, "books", "*.md")))
    book_files = [f for f in book_files if os.path.basename(f) not in skip and os.path.basename(f) != "index.md"]
    
    blog_files = sorted(glob.glob(os.path.join(REPO, "blog", "*.html")))
    
    core_pages = []
    for name in ["index.md", "about.md", "contact.md", "books/index.md"]:
        fp = os.path.join(REPO, name)
        if os.path.exists(fp):
            core_pages.append(fp)
    
    # ═══ Process all files ═══
    total_changed = 0
    
    print("═══ BOOK PAGES ═══")
    for f in book_files:
        changed, what = fix_file(f)
        if changed:
            total_changed += 1
            print(f"  ✓ {os.path.basename(f)}: {', '.join(what)}")
        else:
            print(f"  · {os.path.basename(f)}: no changes")
    
    print(f"\n═══ BLOG POSTS ({len(blog_files)} files) ═══")
    for f in blog_files:
        changed, what = fix_file(f)
        if changed:
            total_changed += 1
            print(f"  ✓ {os.path.basename(f)}: {', '.join(what)}")
        else:
            print(f"  · {os.path.basename(f)}: no changes")
    
    print("\n═══ CORE PAGES ═══")
    for f in core_pages:
        changed, what = fix_file(f)
        if changed:
            total_changed += 1
            print(f"  ✓ {os.path.basename(f)}: {', '.join(what)}")
        else:
            print(f"  · {os.path.basename(f)}: no changes")
    
    # ═══ Blog index (blog.md) — special handling ═══
    blog_index = os.path.join(REPO, "blog.md")
    if os.path.exists(blog_index):
        changed1, what1 = fix_file(blog_index)
        changed2 = fix_blog_card_page(blog_index)
        if changed1 or changed2:
            total_changed += 1
            print(f"  ✓ blog.md: dark theme + {', '.join(what1) if what1 else 'card CSS'}")
        else:
            print(f"  · blog.md: no changes")
    
    print(f"\n═══ DONE: {total_changed} files updated ═══")


if __name__ == "__main__":
    main()
