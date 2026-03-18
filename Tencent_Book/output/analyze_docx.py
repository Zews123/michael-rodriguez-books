"""
Analyze the structure of Final_Book.docx to understand paragraph styles and order.
"""
from docx import Document

doc = Document("Final_Book.docx")

# Show first 30 paragraphs with their styles
for i, p in enumerate(doc.paragraphs[:40]):
    text = p.text.strip()
    if text:
        preview = text[:80] + ("..." if len(text) > 80 else "")
        print(f"[{i:3d}] style={p.style.name:20s} align={str(p.alignment):10s} | {preview}")
    else:
        print(f"[{i:3d}] style={p.style.name:20s} (empty)")
