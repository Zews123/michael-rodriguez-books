from docx import Document
from docx.oxml.ns import qn

doc = Document("Final_Book.docx")

# Check page breaks and key paragraphs
for i, p in enumerate(doc.paragraphs[:22]):
    text = p.text.strip()
    if not text and p.style.name == "Normal":
        # Check for page break
        has_break = False
        for run in p.runs:
            for br in run._element.findall(qn("w:br")):
                if br.get(qn("w:type")) == "page":
                    has_break = True
        if has_break:
            print(f"[{i:3d}] === PAGE BREAK ===")
        continue
    
    # Check if paragraph contains a page break at end
    has_break = False
    for run in p.runs:
        for br in run._element.findall(qn("w:br")):
            if br.get(qn("w:type")) == "page":
                has_break = True
    
    preview = text[:60] if text else "(empty)"
    brk = " [PAGE BREAK AFTER]" if has_break else ""
    
    # Check subtitle size
    sizes = set()
    for run in p.runs:
        if run.font.size:
            sizes.add(run.font.size)
    size_info = f" size={sizes}" if sizes else ""
    
    print(f"[{i:3d}] {p.style.name:18s} align={str(p.alignment):10s}{size_info} | {preview}{brk}")
