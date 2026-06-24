"""Debug: find exact brace structure around coefficient lists."""
import re

text = open(r'rtl/data/LandscapeData/degree3conductor1r0r0r0.dat', encoding='utf-8').read()
text = re.sub(r'\*\^([-+]?\d+)', r'e\1', text)

# Find a coefficient list candidate: sequence of numbers ending with `
# within a brace block
coeff_candidates = list(re.finditer(r'\d+`\d+\.\*\s*,\s*\d+`', text))
print(f"Found {len(coeff_candidates)} coefficient adjacency candidates")

# Look at the structure of the first entry starting at position 0
# Find the first occurrence of patterns
print("\nChunk from position 260 to 340:")
print(repr(text[260:340]))

print("\nChunk from position 290 to 370:")
print(repr(text[290:370]))

# Now let's look at what's between }} and {1/1000000
# The structure seems to be:
# {{{{{...coeffs...}}}, {1/1000000, 1/1000000000000}, {50, 10}}
# So the coefficient list is followed by }}} and then {tolerance}

# Let's find the pattern: coeff block, then }}}, then {/d
# Try to find entries by matching the END pattern
end_pat = re.compile(r'\}\s*\}\s*\}\s*,\s*\{\s*1/\d+\s*,\s*1/\d+\s*\}')
ends = list(end_pat.finditer(text))
print(f"\nFound {len(ends)} entry-ending patterns")

# Look for the coefficient list before each ending
for idx, m in enumerate(ends[:3]):
    before = text[m.start()-100:m.start()]
    print(f"\nEntry end #{idx}:")
    print(f"  Ending at {m.start()}")
    print(f"  Text before: {repr(before[:80])}")
    # Extract any numeric lists in this region
    nums = re.findall(r'([\d\.\+\-eE]+)`[\d\.\*]*', before)
    print(f"  Numbers found: {nums[-5:] if len(nums) >= 5 else nums}")

# Better approach: extract everything between consecutive entry-ending patterns
print("\n\n=== Attempting full entry extraction ===")
for idx in range(min(3, len(ends))):
    start = ends[idx].start()
    # Find the corresponding entry start by scanning backward
    # The entry structure is: {{{{... between end[i] and end[i+1]
    
    if idx == 0:
        prev_end = 0
    else:
        prev_end = ends[idx-1].end()
    
    entry_text = text[prev_end:ends[idx].end()+10]
    print(f"\nEntry {idx} (from {prev_end} to {ends[idx].end()}):")
    print(f"  First 200 chars: {repr(entry_text[:200])}")
    print(f"  Nested braces check: {{={entry_text.count('{')}, }}={entry_text.count('}')}")
