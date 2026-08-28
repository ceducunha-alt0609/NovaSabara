from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""      const revenueCurrent = classes.reduce((a,c) => a + c.revenueCurrent, 0);
      const revenueRecommended = classes.reduce((a,c) => a + c.revenueRecommended, 0);
      const staffCost = classes.reduce((a,c) => a + c.staffCost, 0);
      const fixed = form.fixed;
      const variableTotal = form.variable * totalEnrolled;
      const totalCost = fixed + variableTotal;
      const monthlyResult = revenueCurrent - totalCost;
      const avgTicketCurrent = totalPayers > 0 ? revenueCurrent / totalPayers : 0;
      const avgTicketRecommended = totalPayers > 0 ? revenueRecommended / totalPayers : 0;
      const occupancy = totalCapacity > 0 ? totalEnrolled / totalCapacity : 0;
      const breakEven = avgTicketCurrent > 0 ? Math.ceil(totalCost / avgTicketCurrent) : 0;
      return {
        classes, form, totalCapacity, totalEnrolled, totalPayers, revenueCurrent,
        revenueRecommended, staffCost, fixed, variableTotal, totalCost,
        monthlyResult, avgTicketCurrent, avgTicketRecommended, occupancy, breakEven
      };
"""
new="""      const revenueCurrentGross = classes.reduce((a,c) => a + c.revenueCurrent, 0);
      const revenueRecommendedGross = classes.reduce((a,c) => a + c.revenueRecommended, 0);
      const staffCost = classes.reduce((a,c) => a + c.staffCost, 0);
      const fixed = form.fixed;
      const variableTotal = form.variable * totalEnrolled;
      const totalCost = fixed + variableTotal;
      const collectionFactor = Math.max(.01, 1 - form.inad);
      const revenueCurrent = revenueCurrentGross * collectionFactor;
      const revenueRecommended = revenueRecommendedGross * collectionFactor;
      const monthlyResult = revenueCurrent - totalCost;
      const avgTicketCurrent = totalPayers > 0 ? revenueCurrentGross / totalPayers : 0;
      const avgTicketRecommended = totalPayers > 0 ? revenueRecommendedGross / totalPayers : 0;
      const occupancy = totalCapacity > 0 ? totalEnrolled / totalCapacity : 0;
      // Ponto de equilíbrio mantém a estrutura atual de matriculados e considera a perda por inadimplência.
      const netTicketCurrent = avgTicketCurrent * collectionFactor;
      const breakEven = netTicketCurrent > 0 ? Math.ceil(totalCost / netTicketCurrent) : 0;
      return {
        classes, form, totalCapacity, totalEnrolled, totalPayers, revenueCurrent,
        revenueRecommended, revenueCurrentGross, revenueRecommendedGross,
        staffCost, fixed, variableTotal, totalCost, collectionFactor,
        monthlyResult, avgTicketCurrent, avgTicketRecommended, occupancy, breakEven
      };
"""
assert old in s, 'precision aggregation anchor not found'
s=s.replace(old,new,1)
old2="""    function estimateScenario(base, occupancyShift, inadShift){
      const adjustedPayers = Math.max(1, Math.round(base.totalPayers * (1 + occupancyShift)));
      const inadFactor = Math.max(.01, 1 - Math.max(0, base.form.inad + inadShift));
      const revenue = base.avgTicketCurrent * adjustedPayers * inadFactor;
      return revenue - base.totalCost;
    }
"""
new2="""    function estimateScenario(base, occupancyShift, inadShift){
      const adjustedPayers = Math.max(1, Math.round(base.totalPayers * (1 + occupancyShift)));
      const adjustedEnrolled = Math.max(1, Math.round(base.totalEnrolled * (1 + occupancyShift)));
      const inadRate = Math.min(.99, Math.max(0, base.form.inad + inadShift));
      const revenue = base.avgTicketCurrent * adjustedPayers * (1 - inadRate);
      const cost = base.fixed + (base.form.variable * adjustedEnrolled);
      return revenue - cost;
    }
"""
assert old2 in s, 'scenario anchor not found'
s=s.replace(old2,new2,1)
old3="""      const studentsToBreakEven = Math.ceil(amountToBreakEven / ticket);
      const studentsToProfit = Math.ceil(amountToGoal / ticket);
      const openSeats = Math.max(0, data.totalCapacity - data.totalEnrolled);
"""
new3="""      // Cada novo aluno também traz custo variável; usar receita líquida de inadimplência menos esse custo.
      const netContribution = Math.max(1, (ticket * data.collectionFactor) - data.form.variable);
      const studentsToBreakEven = Math.ceil(amountToBreakEven / netContribution);
      const studentsToProfit = Math.ceil(amountToGoal / netContribution);
      const openSeats = Math.max(0, data.totalCapacity - data.totalEnrolled);
"""
assert old3 in s, 'enrollment goal anchor not found'
s=s.replace(old3,new3,1)
s=s.replace("        ticket,\n        currentResult,", "        ticket,\n        netContribution,\n        currentResult,",1)
s=s.replace('<div class="line"><span>Receita atual estimada</span><strong>${money.format(data.revenueCurrent)}</strong></div>', '<div class="line"><span>Receita atual líquida estimada</span><strong>${money.format(data.revenueCurrent)}</strong></div>',1)
s=s.replace('<div class="line"><span>Receita adicional necessária</span><strong>${money.format(goalData.amountToGoal)}</strong></div>', '<div class="line"><span>Resultado adicional necessário</span><strong>${money.format(goalData.amountToGoal)}</strong></div>',1)
s=s.replace('<div class="line final"><span>Ticket usado na meta</span><strong>${money.format(goalData.ticket)}</strong></div>', '<div class="line"><span>Ticket usado na meta</span><strong>${money.format(goalData.ticket)}</strong></div>\n        <div class="line final"><span>Contribuição líquida por novo aluno</span><strong>${money.format(goalData.netContribution)}</strong></div>',1)
s=s.replace('Receita atual estimada: ${money.format(d.revenueCurrent)}', 'Receita atual líquida estimada: ${money.format(d.revenueCurrent)}',1)
# Ensure realistic scenario uses the same assumptions path as the other scenarios.
s=s.replace("document.getElementById('scenarioRealistic').textContent = money.format(data.monthlyResult);", "document.getElementById('scenarioRealistic').textContent = money.format(estimateScenario(data, 0, 0));",1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
t,n=re.subn(r"const CACHE_NAME = '[^']+';", "const CACHE_NAME = 'nova-sabara-pwa-v1.0.4-precision-integrity';", t, count=1)
assert n==1
sw.write_text(t,encoding='utf-8')

s=p.read_text(encoding='utf-8')
assert 'const netContribution = Math.max(1' in s
assert 'revenueCurrentGross * collectionFactor' in s
assert 'adjustedEnrolled' in s
