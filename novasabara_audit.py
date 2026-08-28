from pathlib import Path
import re
files=['index.html','sw.js','service-worker.js','manifest.json']
out=[]
for fn in files:
 p=Path(fn)
 if not p.exists(): continue
 s=p.read_text(encoding='utf-8',errors='replace')
 out.append(f'===== {fn} =====\nLINES {s.count(chr(10))+1} SIZE {len(s)}\n')
 for term in ['localStorage','sessionStorage','indexedDB','supabase','firebase','seed','demo','backup','restore','import','export','reset','clear()','removeItem','setItem','toISOString().split','new Date(','mensal','pag','aluno','turma','valor','desconto','multa','juros','venc','serviceWorker.register','caches.delete','location.reload']:
  hits=[m.start() for m in re.finditer(re.escape(term),s,re.I)]
  out.append(f'{term}: {len(hits)}\n')
 out.append('\n')
# contexts from index
s=Path('index.html').read_text(encoding='utf-8',errors='replace')
for term in ['localStorage','seed','backup','restore','import','export','reset','removeItem','toISOString','mensalidade','pagamento','pago','vencimento','multa','juros','desconto','supabase','firebase']:
 out.append(f'\n### {term}\n')
 for m in list(re.finditer(re.escape(term),s,re.I))[:40]:
  a=max(0,m.start()-350); b=min(len(s),m.start()+900)
  out.append(s[a:b]+'\n---\n')
# duplicate function names
names=re.findall(r'(?m)^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(',s)
from collections import Counter
out.append('\n### DUPLICATE FUNCTIONS\n')
for n,c in Counter(names).items():
 if c>1: out.append(f'{n}: {c}\n')
Path('novasabara_audit_report.txt').write_text(''.join(out),encoding='utf-8')
