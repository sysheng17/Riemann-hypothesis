"""Debug: count coefficient lists of various lengths."""
import re

text = open(r'rtl/data/LandscapeData/degree3conductor1r0r0r0.dat', encoding='utf-8').read()
text = re.sub(r'\*\^([-+]?\d+)', r'e\1', text)

# Find all lists of numbers: {num`, num`, ..., num`}
# Count how many numbers in each
list_pattern = re.compile(r'\{([\d\.\+\-eE`,\s\.\*]+)\}')
counts = {}
for m in list_pattern.finditer(text):
    content = m.group(1).strip()
    # Count numbers (things ending with `)
    nums = re.findall(r'[\d\.\+\-eE]+`[\d\.\*]*', content)
    l = len(nums)
    if 3 <= l <= 30:
        counts[l] = counts.get(l, 0) + 1

for k in sorted(counts.keys()):
    print(f'{k}-number lists: {counts[k]}')

# Also look for lists with variable-length content between {{}, {}} and {tol}
# The structure of each entry seems to be:
# {{{{ν1, ν2}, group, type, {coeffs...}}}, {tol1, tol2}, {n1, n2}}
# So coefficient lists may vary in length

# Let me look near position 11503
print(f'\nAt position 11503:')
print(repr(text[11500:11600]))
