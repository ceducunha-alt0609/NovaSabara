from pathlib import Path
import re
s=Path('index.html').read_text(encoding='utf-8')
lines=s.splitlines()
terms=['function updateSmartAlerts','function renderHistory','function addHistory','function saveHistory','function getHistory','HIST_KEY','innerHTML =','localStorage.setItem','localStorage.removeItem','function reset','function updateAdjustmentTable','function getPrecisionData']
out=[]
for term in terms:
    out.append(f'\n## {term}\n')
    hits=[i for i,l in enumerate(lines,1) if term.lower() in l.lower()]
    for i in hits[:40]:
        a=max(1,i-8); b=min(len(lines),i+25)
        out.append(f'-- {a}-{b} --\n')
        out.extend(f'{n}: {lines[n-1]}\n' for n in range(a,b+1))
# duplicate named functions and duplicate ids
names=re.findall(r'(?m)^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(',s)
from collections import Counter
out.append('\n## DUPLICATE FUNCTIONS\n')
for n,c in sorted(Counter(names).items()):
    if c>1: out.append(f'{n}: {c}\n')
ids=re.findall(r'\bid=["\']([^"\']+)["\']',s)
out.append('\n## DUPLICATE IDS\n')
for n,c in sorted(Counter(ids).items()):
    if c>1: out.append(f'{n}: {c}\n')
Path('novasabara_final_findings.txt').write_text(''.join(out),encoding='utf-8')
