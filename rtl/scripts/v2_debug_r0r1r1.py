"""Debug: look at raw r0r1r1 entry structure."""
import re

text = open(r'rtl/data/LandscapeData/degree3conductor1r0r1r1.dat', encoding='utf-8').read()
text = re.sub(r'\*\^([-+]?\d+)', r'e\1', text)

# Find first entry boundary
m = re.search(r'\}\s*,\s*\{\s*1/(\d+)\s*,\s*1/(\d+)\s*\}\s*,\s*\{\s*(\d+)\s*,\s*(\d+)\s*\}', text)
if m:
    # Walk backward from this boundary
    start = m.start()
    
    # The entry starts with {{{{ 
    # Walk back until we find the outer start
    depth = 0
    entry_start = start
    for i in range(start, max(0, start-500), -1):
        if text[i] == '}':
            depth += 1
        elif text[i] == '{':
            depth -= 1
            if depth < 0:
                entry_start = i
                break
    
    entry = text[entry_start:m.end()+5]
    print(f"Entry {entry_start}:{m.end()+5} ({len(entry)} chars)")
    print(entry[:600])
    print("\n---ALL numbers found---")
    nums = re.findall(r'([\d\.\+\-eE]+)`([\d\.\*]*)', entry)
    for i, (n, p) in enumerate(nums):
        print(f"  #{i}: {n}`{p}")
