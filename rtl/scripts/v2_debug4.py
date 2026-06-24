"""Debug: check exact bytes around coefficient block."""
import re

text = open(r'rtl/data/LandscapeData/degree3conductor1r0r0r0.dat', encoding='utf-8').read()
text = re.sub(r'\*\^([-+]?\d+)', r'e\1', text)

# Check line 4 (around coeff list)
lines = text.split('\n')
for i in range(3, 8):
    print(f"Line {i}: {repr(lines[i][:120])}")

# The number format is: 1.0484624522346826052497226229589770788`20.
# Let me test the regex
test = "1.0484624522346826052497226229589770788`20."
m = re.search(r'([\d\.\+\-eE]+)`([\d\.\*]*)', test)
print(f"\nRegex test: {m.groups() if m else 'No match'}")

# Test on the full first coefficient list region
chunk = text[278:400]
print(f"\nChunk 278-400: {repr(chunk)}")

# More test: find 20. pattern  
print(f"\n'20.' count: {text.count('20.')}")
print(f"'20,' count: {text.count('20,')}")

# Actually let me just check: what does the file actually contain
with open(r'rtl/data/LandscapeData/degree3conductor1r0r0r0.dat', encoding='utf-8') as f:
    line = f.readlines()[3]
    print(f"\nRaw line 4: {repr(line[:120])}")

# Check the actual char around `20
idx = text.find('20.')
if idx >= 0:
    print(f"\nAround first '20.': {repr(text[idx-5:idx+10])}")
    
idx = text.find('`20')
if idx >= 0:
    print(f"Around first backtick-20: {repr(text[idx-10:idx+15])}")

# Ahh, maybe the file doesn't have "`20." format. Let me look at the actual
# Mathematica output format. Maybe it's: 20` or something else.
# Let me look at how the numbers actually end
print("\nLooking for digit-backtick patterns:")
for i in range(100):
    m = re.search(r'(\d)`', text[i*1000:(i+1)*1000])
    if m:
        start = i*1000 + m.start()
        print(f"  At {start}: ...{repr(text[start-5:start+15])}...")
        break
