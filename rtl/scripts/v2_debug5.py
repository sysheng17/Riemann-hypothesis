"""Look at r0r1r1 data structure."""
import re

text = open(r'rtl/data/LandscapeData/degree3conductor1r0r1r1.dat', encoding='utf-8').read()
text = re.sub(r'\*\^([-+]?\d+)', r'e\1', text)

# Show full first entry
idx = text.find('{{{')
if idx >= 0:
    print("First tripple-brace at", idx)
    depth = 0
    for i in range(idx, min(idx+2000, len(text))):
        if text[i] == '{': depth += 1
        elif text[i] == '}': depth -= 1
        if depth == 0:
            print("Entry end at", i)
            entry = text[idx:i+1]
            print("Entry length:", len(entry), "chars")
            print(entry[:800])
            break

# Also show 2nd entry
nxt = text.find('{{{', idx+1)
if nxt >= 0:
    print("\n\n2nd entry at", nxt)
    print(text[nxt:nxt+400])
