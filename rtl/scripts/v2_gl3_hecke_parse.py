"""Parse GL(3) data — extract coefficient lists after {{}, {}}."""
import re
import numpy as np
from pathlib import Path

DATA_DIR = Path(r'rtl/data')
LD_DIR = DATA_DIR / 'LandscapeData'

def find_balanced_brace(s, start):
    """Find matching close brace starting from position start (which should be '{')."""
    depth = 0
    for i in range(start, len(s)):
        if s[i] == '{': depth += 1
        elif s[i] == '}': depth -= 1
        if depth == 0:
            return i
    return -1

def extract_coeff_list(text, after_pos):
    """Extract the coefficient list after position after_pos.
    The list looks like: {num1`prec., num2`prec., ..., numN`prec.}
    """
    # Find the next '{'
    start = text.find('{', after_pos)
    if start < 0:
        return None
    
    # Get brace-balanced content
    end = find_balanced_brace(text, start)
    if end < 0:
        return None
    
    block = text[start:end+1]
    # Extract all numbers (format: number`precision)
    nums = re.findall(r'([\d\.\+\-eE]+)`[\d\.\*]*', block)
    if len(nums) >= 10:
        return np.array([float(n) for n in nums])
    return None

def parse_entries(filepath):
    """Parse GL(3) entries using {{}, {}} as anchor before coefficient lists."""
    text = open(filepath, encoding='utf-8').read()
    text = re.sub(r'\*\^([-+]?\d+)', r'e\1', text)
    
    entries = []
    seen_keys = set()
    
    # Find all occurrences of {{}, {}} followed by coefficient lists
    empty_pair = re.compile(r'\{\s*\{\s*\}\s*,\s*\{\s*\}\s*\}')
    
    for m in empty_pair.finditer(text):
        coeffs = extract_coeff_list(text, m.end())
        if coeffs is None:
            continue
        
        # Find spectral params BEFORE this {{}, {}} (within 1000 chars)
        before = text[max(0, m.start()-1000):m.start()]
        sp = re.search(r'\{\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*\}', before)
        if not sp:
            continue
        
        nu1, nu2 = abs(float(sp.group(1))), abs(float(sp.group(2)))
        if nu1 < nu2:
            nu1, nu2 = nu2, nu1
        
        # Filter: Hecke eigenvalues must be in plausible range
        # For generic GL(3) RP conjecture says |A(1,p)| ≤ 3; we allow up to 10
        if np.max(np.abs(coeffs)) > 10:
            continue
        
        # Deduplication
        key = (round(nu1, 4), round(nu2, 4))
        if key not in seen_keys:
            seen_keys.add(key)
            entries.append({
                'nu1': nu1, 'nu2': nu2,
                'coeffs': coeffs,
                'n_coeff': len(coeffs),
            })
    
    print(f"  Extracted {len(entries)} entries")
    return entries

# Parse both files
for fname in ['degree3conductor1r0r0r0.dat', 'degree3conductor1r0r1r1.dat']:
    print(f"\n[{fname}]")
    entries = parse_entries(LD_DIR / fname)
    
    if entries:
        lens = [e['n_coeff'] for e in entries]
        print(f"  Coeff distribution: {sorted([(l, lens.count(l)) for l in set(lens)])}")
        
        all_coeffs = np.concatenate([e['coeffs'] for e in entries])
        print(f"  All coeffs: min={np.min(all_coeffs):.4f}, max={np.max(all_coeffs):.4f}, "
              f"mean={np.mean(all_coeffs):+.4f}, std={np.std(all_coeffs):.4f}")
        
        # Show first few entries
        for i in range(min(3, len(entries))):
            e = entries[i]
            print(f"  #{i}: nu=({e['nu1']:.4f}, {e['nu2']:.4f}), "
                  f"first 8 coeffs: {np.round(e['coeffs'][:8], 4)}")
        
        # Check Ramanujan-Petersson bound |A(1,p)| ≤ 3
        extreme = all_coeffs[np.abs(all_coeffs) > 3]
        print(f"  |coeff| > 3: {len(extreme)}/{len(all_coeffs)} "
              f"({100*len(extreme)/len(all_coeffs):.2f}%)")
        if len(extreme) > 0:
            print(f"    Max |coeff|: {np.max(np.abs(extreme)):.4f}")
        
        # Save
        label = fname.replace('degree3conductor1', '').replace('.dat', '')
        npz_path = DATA_DIR / f'v2_{label}_hecke.npz'
        np.savez(npz_path,
                 nu=np.array([(e['nu1'], e['nu2']) for e in entries]),
                 n_coeff=np.array([e['n_coeff'] for e in entries]),
                 coeffs_flat=np.concatenate([e['coeffs'] for e in entries]),
                 coeff_starts=np.cumsum([0] + [e['n_coeff'] for e in entries[:-1]]))
        print(f"  [Saved] {npz_path}")
