NOVA SABARÁ MENSALIDADES — PWA FINAL

Arquivos principais:
- index.html
- manifest.json
- sw.js
- service-worker.js
- icon-192.png
- icon-512.png
- apple-touch-icon.png
- favicon.png

IMPORTANTE PARA INSTALAÇÃO
1. Suba todos os arquivos para a raiz do repositório.
2. Ative GitHub Pages.
3. Abra a URL publicada em HTTPS.
4. O app registra o service worker em ./sw.js.
5. No Android/Chrome deve aparecer opção de instalar após carregamento.
6. No iPhone/Safari normalmente aparece como "Adicionar à Tela de Início"; isso é o comportamento do iOS.

Se só aparecer "atalho":
- confira se a URL é HTTPS do GitHub Pages;
- confira se sw.js abre sem erro 404;
- confira se manifest.json abre sem erro 404;
- espere alguns segundos com a página aberta;
- feche e abra novamente;
- limpe cache se já havia uma versão anterior.

URL esperada:
https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/
