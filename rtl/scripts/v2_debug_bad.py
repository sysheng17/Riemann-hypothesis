"""Debug: examine entries with extreme coefficient values."""
import re
import numpy as np
from pathlib import Path

LD_DIR = Path(r'rtl/data/LandscapeData')

def find_balanced_brace(s, start):
    depth = 0
    for i in range(start, len(s)):
        if s[i] == '{': depth += 1
        elif s[i] == '}': depth -= 1
        if depth == 0: return i
    return -1

def extract_coeff_list(text, after_pos):
    start = text.find('{', after_pos)
    if start < 0: return None
    end = find_balanced_brace(text, start)
    if end < 0: return None
    block = text[start:end+1]
    nums = re.findall(r'([\d\.\+\-eE]+)`[\d\.\*]*', block)
    if len(nums) >= 10:
        return (start, end, np.array([float(n) for n in nums]))
    return None

text = open(LD_DIR / 'degree3conductor1r0r0r0.dat', encoding='utf-8').read()
text = re.sub(r'\*\^([-+]?\d+)', r'e\1', text)

# Find all coefficient extractions with extreme values
empty_pair = re.compile(r'\{\s*\{\s*\}\s*,\s*\{\s*\}\s*\}')
bad_entries = []
for m in empty_pair.finditer(text):
    result = extract_coeff_list(text, m.end())
    if result is None: continue
    start, end, coeffs = result
    if np.max(np.abs(coeffs)) > 100:
        bad_entries.append((m.start(), start, end, coeffs))
        if len(bad_entries) >= 3:
            break

print(f"Found {len(bad_entries)} entries with extreme values")
for i, (emp_pos, coeff_start, coeff_end, coeffs) in enumerate(bad_entries):
    print(f"\n--- Bad entry #{i} ---")
    print(f"  {{}}, {{}} at {emp_pos}, coeff list at {coeff_start}-{coeff_end}")
    print(f"  Coeffs ({len(coeffs)} values): first 10 = {np.round(coeffs[:10], 4)}")
    print(f"  All coeffs: {np.round(coeffs, 4)}")
    
    # Show context around this entry
    context = text[max(0, coeff_start-200):min(len(text), coeff_end+100)]
    print(f"  Context: ...{repr(context[:150])}...")
    
    # Check what numbers are near the start of the coefficient list
    # There might be a different inner structure
    before = text[emp_pos:coeff_start]
    print(f"  Between {{}}, {{}} and coeff list: {repr(before[:100])}")
