"""
Originality self-check for the manuscript.
Detects: repetitive patterns, AI clichés, structural monotony.
"""
import re
from collections import Counter

text = open("Full_Book_clean.md", encoding="utf-8").read()
paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]

# 1. Detect AI cliché phrases
ai_cliches = [
    "it's worth noting", "it is worth mentioning", "delve into",
    "it's important to note", "in the realm of", "a testament to",
    "the landscape of", "navigate the complex", "paradigm shift",
    "at the end of the day", "in today's world", "game-changer",
    "deep dive", "unpack this", "let that sink in",
    "the question remains", "only time will tell", "a far cry from",
    "sends a clear message", "raises important questions",
    "the elephant in the room", "tip of the iceberg",
    "a double-edged sword", "the writing is on the wall",
    "a perfect storm", "the bottom line", "remains to be seen",
    "it bears mentioning", "it cannot be overstated",
    "a cautionary tale", "the implications are profound",
    "it goes without saying", "needless to say", "in essence",
    "at its core", "when all is said and done", "the fact remains",
    "in no uncertain terms", "for better or worse", "by and large",
    "the stakes are high", "what sets .* apart", "the irony is",
    "speaks volumes", "begs the question", "food for thought",
    "a wake-up call", "the writing on the wall", "hindsight is 20/20",
    "a slippery slope", "the bigger picture", "a pivotal moment"
]

cliche_count = 0
cliche_instances = []
text_lower = text.lower()
for phrase in ai_cliches:
    count = text_lower.count(phrase)
    if count > 0:
        cliche_count += count
        cliche_instances.append(f"  '{phrase}' x{count}")

# 2. Detect repetitive sentence starters (first 3 words)
starters = []
sentences = re.split(r'[.!?]\s+', text)
for s in sentences:
    words = s.strip().split()[:3]
    if len(words) == 3:
        starters.append(" ".join(words).lower())

starter_counts = Counter(starters)
repetitive_starters = [(s, c) for s, c in starter_counts.most_common(30) if c > 5]

# 3. Detect paragraph length monotony
para_lengths = [len(p.split()) for p in paragraphs]
avg_len = sum(para_lengths) / len(para_lengths) if para_lengths else 0
monotone = sum(1 for l in para_lengths if abs(l - avg_len) < 10) / len(para_lengths) * 100

# 4. Check for "the most" / "the world's" overuse
superlative_phrases = [
    "the most powerful", "the most important", "the most valuable",
    "the world's largest", "the world's most", "the biggest",
    "the single most", "one of the most", "the greatest"
]
superlative_count = 0
superlative_instances = []
for phrase in superlative_phrases:
    count = text_lower.count(phrase)
    if count > 0:
        superlative_count += count
        superlative_instances.append(f"  '{phrase}' x{count}")

# 5. Check for repetitive transition phrases
transitions = [
    "but here's the", "the reality is", "the truth is",
    "in other words", "to put it", "what this means",
    "the result was", "the answer was", "this was the moment",
    "this is not", "this is the", "this was not", "this was the",
    "and it was", "but it was", "it was a", "it was the",
    "there was a", "there were", "there is a"
]
transition_count = 0
transition_instances = []
for phrase in transitions:
    count = text_lower.count(phrase)
    if count > 3:
        transition_count += count
        transition_instances.append(f"  '{phrase}' x{count}")

# 6. Report
print("=" * 50)
print("ORIGINALITY SELF-CHECK REPORT")
print("=" * 50)
print(f"File: Full_Book_clean.md")
print(f"Paragraphs analyzed: {len(paragraphs)}")
print(f"Total sentences: {len(sentences)}")
print(f"Average paragraph length: {avg_len:.0f} words")
print()

print("--- 1. AI CLICHÉ PHRASES ---")
if cliche_count == 0:
    print("[PASS] No AI cliché phrases detected")
elif cliche_count <= 5:
    print(f"[WARN] {cliche_count} AI cliché phrases found:")
    for c in cliche_instances:
        print(c)
else:
    print(f"[FAIL] {cliche_count} AI cliché phrases found — REWRITE needed:")
    for c in cliche_instances:
        print(c)

print()
print("--- 2. REPETITIVE SENTENCE STARTERS ---")
if not repetitive_starters:
    print("[PASS] No repetitive sentence starters (threshold: >5)")
else:
    print(f"[WARN] {len(repetitive_starters)} repetitive starters detected:")
    for s, c in repetitive_starters:
        print(f"  '{s}...' x{c}")

print()
print("--- 3. PARAGRAPH LENGTH VARIETY ---")
if monotone < 40:
    print(f"[PASS] Good variety ({monotone:.0f}% similar length)")
else:
    print(f"[WARN] Too uniform ({monotone:.0f}% similar) — vary paragraph structure")

print()
print("--- 4. SUPERLATIVE OVERUSE ---")
if superlative_count <= 10:
    print(f"[PASS] Superlatives OK ({superlative_count} instances)")
else:
    print(f"[WARN] {superlative_count} superlative phrases — consider reducing:")
    for s in superlative_instances:
        print(s)

print()
print("--- 5. REPETITIVE TRANSITIONS ---")
if transition_count == 0:
    print("[PASS] No overused transition phrases")
else:
    print(f"[WARN] {transition_count} overused transitions:")
    for t in transition_instances:
        print(t)

print()
print("=" * 50)
all_good = cliche_count <= 5 and not repetitive_starters and monotone < 40 and superlative_count <= 15
if all_good:
    print("OVERALL: [PASS] — Ready for external verification")
else:
    print("OVERALL: [WARN] — Review flagged items before upload")
print("=" * 50)
