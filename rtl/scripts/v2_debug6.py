"""Debug the coefficient extraction regex."""
import re

text = open(r'rtl/data/LandscapeData/degree3conductor1r0r0r0.dat', encoding='utf-8').read()
text = re.sub(r'\*\^([-+]?\d+)', r'e\1', text)

# Find first {{}, {}} and what follows
idx = text.find('{{}, {}}')
if idx >= 0:
    print("Found first {{}, {}} at", idx)
    after = text[idx:idx+300]
    print("After (300 chars):")
    print(repr(after))
    
    # What we want: {{}, {}}, {num, num, ..., num}}}, {
    # The coefficient block is inside: {num, num, ..., num}
    # It's followed by }}}, {
    
    # Approach: find {{}, {}} and locate the coefficient block after it
    # The coefficient block is {num1, num2, ..., numN}
    # followed by }}}, { (which is the tolerance block)
    
    # Find the block between {{}, {}}, and }}}, {
    m = re.search(r'\{\s*\{\s*\}\s*,\s*\{\s*\}\s*\}\s*,\s*(\{[\s\S]*?\}\s*\}\s*,\s*\{)', text[idx:idx+500])
    if m:
        blk = m.group(1)
        print("\nMatched block:")
        print(blk[:200])
    else:
        print("\nNo match!")
        
        # Try step by step
        print("\nStep-by-step matching:")
        step1 = re.search(r'\{\s*\{\s*\}\s*,\s*\{\s*\}\s*\}', text[idx:idx+100])
        if step1:
            print("  Step 1 OK:", repr(step1.group()))
        else:
            print("  Step 1 FAIL")
