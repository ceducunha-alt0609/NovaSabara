from pathlib import Path
import re
s=Path('index.html').read_text(encoding='utf-8',errors='replace').splitlines()
terms=['function collectState','function applyState','function exportBackup','function importBackup','function clearSavedData','HIST_KEY','function loadHistory','function saveHistory','function clearHistory','function saveHistoryEntry','serviceWorker.register','novaSabaraCalculadoraState']
out=[]
for term in terms:
 out.append(f'\n## {term}\n')
 for i,line in enumerate(s,1):
  if term.lower() in line.lower():
   a=max(1,i-3); b=min(len(s),i+22)
   for j in range(a,b+1): out.append(f'{j}: {s[j-1]}\n')
   out.append('---\n')
for fn in ['sw.js','service-worker.js']:
 p=Path(fn)
 if p.exists():
  out.append(f'\n## {fn}\n')
  for i,line in enumerate(p.read_text(encoding="utf-8",errors="replace").splitlines(),1): out.append(f'{i}: {line}\n')
Path('novasabara_findings.txt').write_text(''.join(out),encoding='utf-8')
