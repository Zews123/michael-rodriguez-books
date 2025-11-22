# Schema Markup Validation Guide
## How to Test Your Schema Markup

This guide provides step-by-step instructions for validating the Schema Markup on the Michael Rodriguez Books website.

---

## Quick Testing Checklist

- [ ] Test homepage with Google Rich Results Test
- [ ] Test about page with Google Rich Results Test
- [ ] Test contact page with Google Rich Results Test
- [ ] Test at least 3 book pages with Google Rich Results Test
- [ ] Test at least 2 blog pages with Google Rich Results Test
- [ ] Validate JSON-LD syntax with Schema.org Validator
- [ ] Check Google Search Console for rich result enhancements
- [ ] Monitor performance over 2-4 weeks

---

## 1. Google Rich Results Test

**URL:** https://search.google.com/test/rich-results

### How to Use:
1. Go to https://search.google.com/test/rich-results
2. Enter your page URL (e.g., `https://zews123.github.io/michael-rodriguez-books/about`)
3. Click "TEST URL"
4. Wait for results (usually 10-30 seconds)
5. Review detected schema types and any errors

### Pages to Test:

#### Priority 1: Key Pages
```
✅ Homepage
https://zews123.github.io/michael-rodriguez-books/

✅ About Page (Person Schema)
https://zews123.github.io/michael-rodriguez-books/about

✅ Contact Page (ContactPage Schema)
https://zews123.github.io/michael-rodriguez-books/contact
```

#### Priority 2: Book Pages (Book Schema)
```
✅ The Profit Machine
https://zews123.github.io/michael-rodriguez-books/books/Profit_Machine

✅ The Bush Machine
https://zews123.github.io/michael-rodriguez-books/books/Bush_Machine

✅ The India Paradox
https://zews123.github.io/michael-rodriguez-books/books/India_Paradox
```

#### Priority 3: Blog Pages (FAQPage Schema)
```
✅ Oil Weapon FAQ
https://zews123.github.io/michael-rodriguez-books/blog/oil-weapon-faq

✅ AI Emperor FAQ
https://zews123.github.io/michael-rodriguez-books/blog/AI-Emperor-FAQ
```

### Expected Results:

#### Homepage
- **Schema Type:** FAQPage
- **Status:** ✅ Eligible for rich results
- **Rich Result Type:** FAQ accordion in search results

#### About Page
- **Schema Type:** Person
- **Status:** ✅ Valid (may show "Not eligible for rich results" - this is normal)
- **Purpose:** Knowledge Graph, author attribution

#### Contact Page
- **Schema Type:** ContactPage
- **Status:** ✅ Valid (may show "Not eligible for rich results" - this is normal)
- **Purpose:** Contact information structure

#### Book Pages
- **Schema Types:** Book, FAQPage
- **Status:** ✅ Eligible for rich results
- **Rich Result Types:** 
  - Book details in Google Books
  - FAQ accordion in search results
  - Author attribution

#### Blog Pages
- **Schema Type:** FAQPage
- **Status:** ✅ Eligible for rich results
- **Rich Result Type:** FAQ accordion in search results

---

## 2. Schema.org Validator

**URL:** https://validator.schema.org/

### How to Use:
1. Go to https://validator.schema.org/
2. Choose "Code Snippet" tab
3. Copy the JSON-LD code from your page source
4. Paste into the validator
5. Click "RUN TEST"
6. Review any errors or warnings

### Extract JSON-LD Code:

**Method 1: View Page Source**
1. Visit your page
2. Right-click → "View Page Source"
3. Search for `<script type="application/ld+json">`
4. Copy the entire JSON block (from `{` to `}`)
5. Paste into validator

**Method 2: Use Browser DevTools**
1. Visit your page
2. Press F12 to open DevTools
3. Go to Elements/Inspector tab
4. Search for `application/ld+json`
5. Copy the JSON content
6. Paste into validator

### Pages to Validate:

```
1. about.md → Person schema
2. contact.md → ContactPage schema
3. _layouts/default.html → Organization + WebSite schema
4. books/Profit_Machine.md → Book + FAQPage schema
5. index.md → FAQPage schema
```

---

## 3. Google Search Console

**URL:** https://search.google.com/search-console

### Setup (if not already done):
1. Go to Google Search Console
2. Add property: `https://zews123.github.io/michael-rodriguez-books/`
3. Verify ownership (use HTML file verification method)
4. Wait 24-48 hours for data collection

### Check Rich Results:
1. Log in to Google Search Console
2. Navigate to "Enhancements" in left sidebar
3. Check these sections:
   - **FAQ** - Should show eligible pages
   - **Books** - Should show book pages (if available)
   - **Unparsed structured data** - Check for Person/Organization schemas

### Monitor Issues:
- Look for "Errors" or "Valid with warnings"
- Fix any reported issues
- Request re-indexing after fixes

### Expected Timeline:
- **Week 1:** Data starts appearing
- **Week 2-3:** Rich results may start showing in search
- **Week 4+:** Full rich result coverage

---

## 4. Bing Webmaster Tools

**URL:** https://www.bing.com/webmasters

### Setup:
1. Sign in to Bing Webmaster Tools
2. Add site: `https://zews123.github.io/michael-rodriguez-books/`
3. Verify ownership
4. Submit sitemap: `https://zews123.github.io/michael-rodriguez-books/sitemap.xml`

### Check Schema:
1. Go to "Site Scan" → "SEO"
2. Look for structured data reports
3. Check for any schema-related warnings

---

## 5. Manual Visual Inspection

### Check JSON-LD Syntax:
Open each modified file and verify:

**✅ about.md:**
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "...",
  "name": "Michael Rodriguez",
  ...
}
```

**✅ contact.md:**
```json
{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  ...
}
```

**✅ _layouts/default.html:**
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      ...
    },
    {
      "@type": "WebSite",
      ...
    }
  ]
}
```

### Common Issues to Check:
- ❌ Missing closing braces `}`
- ❌ Missing commas between properties
- ❌ Unescaped quotes in text
- ❌ Invalid dates format (should be YYYY-MM-DD)
- ❌ Invalid URLs (must be absolute URLs)

---

## 6. Testing with Browser Extensions

### Recommended Extensions:

**Chrome/Edge:**
1. **Schema.org Validator** - Quick inline validation
2. **Structured Data Testing Tool** - Google's official extension
3. **SEO Minion** - Multiple SEO checks including schema

**Firefox:**
1. **Schema Extractor** - Extract and validate schema
2. **SEO Peek** - View structured data

### How to Use:
1. Install extension
2. Visit your page
3. Click extension icon
4. Review detected schema types
5. Check for errors/warnings

---

## 7. Python Validation Script

For automated validation, use this Python script:

```python
#!/usr/bin/env python3
"""
Schema Markup Validator for Michael Rodriguez Books
"""

import json
import re
from urllib.request import urlopen
from urllib.error import URLError

def extract_jsonld(html):
    """Extract JSON-LD from HTML"""
    pattern = r'<script type="application/ld\+json">(.*?)</script>'
    matches = re.findall(pattern, html, re.DOTALL)
    return matches

def validate_jsonld(jsonld_str):
    """Validate JSON-LD syntax"""
    try:
        data = json.loads(jsonld_str)
        return True, data, None
    except json.JSONDecodeError as e:
        return False, None, str(e)

def test_url(url):
    """Test a URL for Schema Markup"""
    print(f"\nTesting: {url}")
    print("=" * 60)
    
    try:
        response = urlopen(url)
        html = response.read().decode('utf-8')
        
        jsonld_blocks = extract_jsonld(html)
        
        if not jsonld_blocks:
            print("❌ No JSON-LD found")
            return False
        
        print(f"✅ Found {len(jsonld_blocks)} JSON-LD block(s)")
        
        for i, block in enumerate(jsonld_blocks, 1):
            print(f"\n--- Block {i} ---")
            valid, data, error = validate_jsonld(block)
            
            if valid:
                print(f"✅ Valid JSON-LD")
                if isinstance(data, dict):
                    schema_type = data.get('@type', 'Unknown')
                    print(f"   Type: {schema_type}")
                    if '@graph' in data:
                        types = [item.get('@type', 'Unknown') for item in data['@graph']]
                        print(f"   Graph Types: {', '.join(types)}")
            else:
                print(f"❌ Invalid JSON-LD: {error}")
                return False
        
        return True
        
    except URLError as e:
        print(f"❌ Error fetching URL: {e}")
        return False

def main():
    """Main test function"""
    base_url = "https://zews123.github.io/michael-rodriguez-books"
    
    test_urls = [
        f"{base_url}/",
        f"{base_url}/about",
        f"{base_url}/contact",
        f"{base_url}/books/Profit_Machine",
        f"{base_url}/books/Bush_Machine",
        f"{base_url}/blog/oil-weapon-faq",
    ]
    
    print("Schema Markup Validation Test")
    print("=" * 60)
    
    results = []
    for url in test_urls:
        result = test_url(url)
        results.append((url, result))
    
    print("\n\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for url, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {url}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
```

**To Run:**
```bash
python3 schema_validator.py
```

---

## 8. Expected Search Result Enhancements

### Before Rich Results:
```
Michael Rodriguez Books
https://zews123.github.io/michael-rodriguez-books
Official website of Michael Rodriguez, economic analyst...
```

### After Rich Results (4-6 weeks):

#### Homepage with FAQ:
```
Michael Rodriguez Books
https://zews123.github.io/michael-rodriguez-books
Official website of Michael Rodriguez...

▼ What books does Michael Rodriguez write about financial crime?
▼ Who is Michael Rodriguez and what is his expertise?
▼ What is the shadow economy and how big is it?
```

#### Book Page:
```
The Profit Machine - Michael Rodriguez
https://zews123.github.io/.../books/Profit_Machine
⭐⭐⭐⭐⭐ · $4.99 · In stock
How defense contractors profit billions from wars...

▼ What makes this military-industrial complex investigation unique?
▼ Does the book expose specific companies profiting from war?
```

---

## 9. Troubleshooting

### Issue: "No eligible rich results found"
**Solution:** This is normal for some schema types (Person, Organization, ContactPage). They still help SEO but don't show as rich snippets.

### Issue: "Invalid JSON-LD syntax"
**Solution:** 
1. Copy the JSON-LD code
2. Paste into https://jsonlint.com
3. Fix syntax errors (missing commas, quotes, etc.)
4. Re-test

### Issue: "Missing required property"
**Solution:** Check schema.org documentation for required properties for your schema type.

### Issue: "URL doesn't match @id"
**Solution:** Ensure all URLs use absolute URLs with proper base URL.

### Issue: "Duplicate @id"
**Solution:** Each entity should have a unique @id. Check for conflicts.

---

## 10. Monitoring and Maintenance

### Weekly Tasks:
- [ ] Check Google Search Console for new errors
- [ ] Monitor rich result impressions
- [ ] Check for broken schema on new pages

### Monthly Tasks:
- [ ] Run full validation on all pages
- [ ] Update schema if content changes
- [ ] Review competitor schema implementations

### When Adding New Content:
- [ ] Add appropriate schema to new pages
- [ ] Validate before publishing
- [ ] Request indexing in Search Console

---

## Validation Checklist

Use this checklist to track your validation progress:

### Initial Validation (Week 1)
- [ ] Test all pages with Google Rich Results Test
- [ ] Validate JSON-LD syntax with Schema.org Validator
- [ ] Fix any errors found
- [ ] Re-test after fixes
- [ ] Submit sitemap to Google Search Console

### Ongoing Monitoring (Weekly)
- [ ] Check Search Console for errors
- [ ] Monitor rich result impressions
- [ ] Check for new warnings

### Monthly Review
- [ ] Review rich result performance
- [ ] Compare with previous month
- [ ] Identify improvement opportunities
- [ ] Update schema if needed

---

## Resources

### Official Documentation:
- Schema.org: https://schema.org/
- Google Search Central: https://developers.google.com/search/docs/appearance/structured-data
- Google Rich Results Test: https://search.google.com/test/rich-results

### Schema Types Used:
- Person: https://schema.org/Person
- Organization: https://schema.org/Organization
- Book: https://schema.org/Book
- FAQPage: https://schema.org/FAQPage
- ContactPage: https://schema.org/ContactPage
- WebSite: https://schema.org/WebSite

### Tools:
- Schema Markup Generator: https://technicalseo.com/tools/schema-markup-generator/
- JSON-LD Playground: https://json-ld.org/playground/
- Structured Data Linter: http://linter.structured-data.org/

---

## Success Metrics

Track these metrics to measure schema markup success:

### Search Console Metrics:
- Rich result impressions (target: increase by 20-30%)
- Average position (target: improve by 2-3 positions)
- Click-through rate (target: increase by 15-25%)

### Google Analytics:
- Organic search traffic (target: increase by 10-15%)
- Bounce rate (target: decrease by 5-10%)
- Pages per session (target: increase by 10-15%)

---

**Last Updated:** November 22, 2025  
**Version:** 1.0
