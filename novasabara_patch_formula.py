from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""      const custoFixoAluno = fixed / pagantes;
      const custoTotalAluno = custoFixoAluno + variable;
      const minima = roundTo(custoTotalAluno, arredondar);
      const seguraBase = custoTotalAluno / Math.max(.01, (1 - inad));
      const segura = roundTo(seguraBase * (1 + reserva), arredondar);
      const ideal = roundTo(segura * (1 + margem), arredondar);

      const receitaMinima = minima * pagantes;
      const receitaSegura = segura * pagantes;
      const receitaIdeal = ideal * pagantes;
      const custoTotalEscola = fixed + (variable * alunos);
      const lucroIdeal = receitaIdeal - custoTotalEscola;
"""
new="""      // Custos variáveis existem para todos os alunos ativos, inclusive bolsistas.
      // A mensalidade mínima precisa ratear o custo total da escola entre os pagantes.
      const custoTotalEscola = fixed + (variable * alunos);
      const custoFixoAluno = fixed / pagantes;
      const custoTotalAluno = custoTotalEscola / pagantes;
      const minima = roundTo(custoTotalAluno, arredondar);
      const seguraBase = custoTotalAluno / Math.max(.01, (1 - inad));
      const segura = roundTo(seguraBase * (1 + reserva), arredondar);
      const ideal = roundTo(segura * (1 + margem), arredondar);

      const receitaMinima = minima * pagantes;
      const receitaSegura = segura * pagantes;
      const receitaIdeal = ideal * pagantes;
      const lucroIdeal = receitaIdeal - custoTotalEscola;
"""
assert old in s, 'formation formula anchor not found'
s=s.replace(old,new,1)
s=s.replace('<div class="line"><span>Custo total por aluno</span><strong>${money.format(c.custoTotalAluno)}</strong></div>', '<div class="line"><span>Custo total rateado por pagante</span><strong>${money.format(c.custoTotalAluno)}</strong></div>',1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
import re
t,n=re.subn(r"const CACHE_NAME = '[^']+';", "const CACHE_NAME = 'nova-sabara-pwa-v1.0.2-formula-integrity';", t, count=1)
assert n==1, 'sw cache anchor not found'
sw.write_text(t,encoding='utf-8')

# Static integrity checks
s=p.read_text(encoding='utf-8')
assert 'const custoTotalEscola = fixed + (variable * alunos);' in s
assert 'const custoTotalAluno = custoTotalEscola / pagantes;' in s
assert s.count('const custoTotalEscola = fixed + (variable * alunos);') == 1
assert 'Custo total rateado por pagante' in s
