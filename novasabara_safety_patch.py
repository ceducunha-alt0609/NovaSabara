from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
old="""    function applyState(state){
      if(!state) return;
      isRestoringState = true;"""
new="""    function isValidSavedState(state){
      return !!(state && typeof state==='object' && !Array.isArray(state) &&
        state.inputs && typeof state.inputs==='object' && !Array.isArray(state.inputs) &&
        state.checks && typeof state.checks==='object' && !Array.isArray(state.checks) &&
        (!('customActivities' in state) || Array.isArray(state.customActivities)) &&
        (!('history' in state) || Array.isArray(state.history)));
    }

    function applyState(state){
      if(!isValidSavedState(state)) throw new Error('Estrutura de dados inválida');
      isRestoringState = true;"""
assert old in s; s=s.replace(old,new,1)
old="""    function exportBackup(){
      const blob = new Blob([JSON.stringify(collectState(), null, 2)], {type:'application/json'});"""
new="""    function exportBackup(){
      const state = collectState();
      try{
        const historyRaw = localStorage.getItem('novaSabaraHistorico_v2');
        state.history = historyRaw ? JSON.parse(historyRaw) : [];
        if(!Array.isArray(state.history)) state.history = [];
      }catch(e){ state.history = []; }
      const blob = new Blob([JSON.stringify(state, null, 2)], {type:'application/json'});"""
assert old in s; s=s.replace(old,new,1)
old="""          const state = JSON.parse(reader.result);
          applyState(state);
          saveState();
          showToast('Backup importado!');"""
new="""          const state = JSON.parse(reader.result);
          if(!isValidSavedState(state)) throw new Error('Estrutura de backup inválida');
          applyState(state);
          if(Array.isArray(state.history)) localStorage.setItem('novaSabaraHistorico_v2', JSON.stringify(state.history));
          saveState();
          if(typeof renderHistory==='function') renderHistory();
          showToast('Backup importado!');"""
assert old in s; s=s.replace(old,new,1)
old="""        localStorage.removeItem('novaSabaraCalculadoraState');
        showToast('Dados locais limpos!');"""
new="""        localStorage.removeItem('novaSabaraCalculadoraState');
        localStorage.removeItem('novaSabaraHistorico_v2');
        showToast('Dados locais limpos!');
        setTimeout(()=>location.reload(), 250);"""
assert old in s; s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

for fn in ['sw.js','service-worker.js']:
 p=Path(fn)
 if not p.exists(): continue
 s=p.read_text(encoding='utf-8')
 if "const CACHE_PREFIX = 'nova-sabara-';" not in s:
  s=s.replace("const CACHE_NAME = ", "const CACHE_PREFIX = 'nova-sabara-';\nconst CACHE_NAME = ",1)
 s=s.replace("keys.map((key) => {\n      if (key !== CACHE_NAME) return caches.delete(key);\n    })", "keys.filter((key) => key.startsWith(CACHE_PREFIX) && key !== CACHE_NAME).map((key) => caches.delete(key))")
 s=s.replace("keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))", "keys.filter(key => key.startsWith(CACHE_PREFIX) && key !== CACHE_NAME).map(key => caches.delete(key))")
 if fn=='sw.js': s=s.replace("nova-sabara-pwa-v1.0.0","nova-sabara-pwa-v1.1-audit-safety",1)
 p.write_text(s,encoding='utf-8')
