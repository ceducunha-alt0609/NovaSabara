from pathlib import Path
import re
s=Path('index.html').read_text(encoding='utf-8')
lines=s.splitlines()
terms=['getCommercialCalc','getFormationCalc','getPrecisionData','commercialTable','desconto','reajuste','ipca','mensalidade','formacao','segura','minima','recommendedPrice','currentPrice','saveHistory','renderHistory','history.push','customActivities']
out=[]
for term in terms:
    out.append(f'\n## {term}\n')
    hits=[i for i,l in enumerate(lines,1) if term.lower() in l.lower()]
    for i in hits[:40]:
        a=max(1,i-12); b=min(len(lines),i+28)
        out.append(f'-- lines {a}-{b} --\n')
        out.extend(f'{n}: {lines[n-1]}\n' for n in range(a,b+1))
# duplicate named functions
names=re.findall(r'(?m)^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(',s)
from collections import Counter
out.append('\n## DUPLICATE FUNCTIONS\n')
for n,c in sorted(Counter(names).items()):
    if c>1: out.append(f'{n}: {c}\n')
Path('novasabara_formula_findings.txt').write_text(''.join(out),encoding='utf-8')
