from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('<label>Margem de lucro desejada (%)</label>', '<label>Acréscimo desejado sobre mensalidade segura (%)</label>', 1)
s=s.replace('<em>Com margem de lucro</em>', '<em>Com acréscimo gerencial</em>', 1)
s=s.replace('<tr><td>Margem desejada</td><td>${(c.margem*100).toFixed(1)}%</td></tr>', '<tr><td>Acréscimo desejado</td><td>${(c.margem*100).toFixed(1)}%</td></tr>', 1)
s=s.replace('A ideal considera margem para crescimento, melhorias e reinvestimento.', 'A ideal considera acréscimo gerencial para crescimento, melhorias e reinvestimento.', 1)

old="""      const receitaMinima = minima * pagantes;
      const receitaSegura = segura * pagantes;
      const receitaIdeal = ideal * pagantes;
      const lucroIdeal = receitaIdeal - custoTotalEscola;

      return {
        fixed, variable, alunos, pagantes, inad, reserva, margem, arredondar,
        custoFixoAluno, custoTotalAluno, minima, segura, ideal,
        receitaMinima, receitaSegura, receitaIdeal, custoTotalEscola, lucroIdeal
      };
"""
new="""      const receitaMinima = minima * pagantes;
      const receitaSegura = segura * pagantes;
      const receitaIdeal = ideal * pagantes;
      // Resultado esperado considera a própria inadimplência informada no cenário.
      const receitaIdealLiquida = receitaIdeal * (1 - inad);
      const lucroIdeal = receitaIdealLiquida - custoTotalEscola;

      return {
        fixed, variable, alunos, pagantes, inad, reserva, margem, arredondar,
        custoFixoAluno, custoTotalAluno, minima, segura, ideal,
        receitaMinima, receitaSegura, receitaIdeal, receitaIdealLiquida, custoTotalEscola, lucroIdeal
      };
"""
assert old in s, 'financial result anchor not found'
s=s.replace(old,new,1)
s=s.replace('const margemReal = c.receitaIdeal > 0 ? (c.lucroIdeal / c.receitaIdeal) * 100 : 0;', 'const margemReal = c.receitaIdealLiquida > 0 ? (c.lucroIdeal / c.receitaIdealLiquida) * 100 : 0;',1)
s=s.replace('<div class="line positive"><span>Receita ideal estimada</span><strong>${money.format(c.receitaIdeal)}</strong></div>', '<div class="line positive"><span>Receita ideal líquida estimada</span><strong>${money.format(c.receitaIdealLiquida)}</strong></div>',1)
s=s.replace('Receita ideal estimada: ${money.format(c.receitaIdeal)}', 'Receita ideal líquida estimada: ${money.format(c.receitaIdealLiquida)}',1)
s=s.replace('<tr><td>Receita ideal estimada</td><td>${money.format(c.receitaIdeal)}</td></tr>', '<tr><td>Receita ideal líquida estimada</td><td>${money.format(c.receitaIdealLiquida)}</td></tr>',1)

assert 'receitaIdealLiquida = receitaIdeal * (1 - inad)' in s
assert 'Acréscimo desejado sobre mensalidade segura (%)' in s
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
t,n=re.subn(r"const CACHE_NAME = '[^']+';", "const CACHE_NAME = 'nova-sabara-pwa-v1.0.3-financial-semantics';", t, count=1)
assert n==1
sw.write_text(t,encoding='utf-8')
