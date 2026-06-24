"""Debug GL(3) Mathematica data format."""
import re

text = open(r'rtl/data/LandscapeData/degree3conductor1r0r0r0.dat', encoding='utf-8').read()
# Normalize scientific notation
text = re.sub(r'\*\^([-+]?\d+)', r'e\1', text)

# Show around first {{}, {}}
idx = text.find('{{}, {}}')
print(f'First {{}}, {{}} at position {idx}')
if idx >= 0:
    print('---Before---')
    print(text[idx-100:idx])
    print('---After---')
    print(text[idx:idx+300])

# Test coefficient regex on a known coefficient list
# Find {{}, {}} and then look for the coefficient list
pattern = r'\{\s*\{\s*\}\s*,\s*\{\s*\}\s*\}'
for m in re.finditer(pattern, text):
    end = m.end()
    after = text[end:end+400]
    print(f'\n{{}}, {{}} at {m.start()}:{end}')
    print(f'Next 400 chars:\n{after[:200]}')
    break  # just first one

# Try simpler coeff list pattern: find 12-number lists
coeff12 = r'\{\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*\}'
print('\nSearching for 12-number coefficient lists...')
count = 0
for m in re.finditer(coeff12, text):
    if count < 3:
        print(f'Found at {m.start()}: [{m.group(1)[:8]}, {m.group(2)[:8]}, {m.group(3)[:8]}, ...]')
    count += 1
print(f'Total 12-coefficient lists: {count}')

# Try 10-number coefficient lists 
coeff10 = r'\{\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*,\s*([\d\.\+\-eE]+)`[\d\.\*]+\s*\}'
print('\nSearching for 10-number coefficient lists...')
count10 = 0
for m in re.finditer(coeff10, text):
    if count10 < 2:
        print(f'Found at {m.start()}: [{m.group(1)[:8]}, {m.group(2)[:8]}, ...]')
    count10 += 1
print(f'Total 10-coefficient lists: {count10}')
