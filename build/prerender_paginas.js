// Renderiza cada página de paginas/ com o TTSCModelKit do design system e grava o HTML resultante.
// Uso: node build/prerender_paginas.js   (requer o Chromium do ambiente, em /opt/pw-browsers)
// O HTML final tem o markup real do design system (sem CSS próprio) e mantém components/bundle.js,
// para que as abas, filtros e gavetas continuem funcionando.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const PAG = path.join(ROOT, 'paginas');
const arquivos = [];
(function w(d) { for (const f of fs.readdirSync(d).sort()) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? w(p) : (f.endsWith('.html') && f !== 'index.html' && arquivos.push(p)); } })(PAG);

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const pg = await b.newPage({ viewport: { width: 1440, height: 900 } });
  let feitas = 0, falhas = [];
  for (const arq of arquivos) {
    const src = fs.readFileSync(arq, 'utf8');
    const m = src.match(/<main[^>]*id="main-viewport"[\s\S]*?<\/main>/);
    if (!m || !/TTSCModelKit\.render/.test(src)) continue; // já estático ou sem especificação
    await pg.goto('file://' + arq, { waitUntil: 'load' });
    await pg.waitForFunction(() => document.querySelector('#model-page #view-table tbody tr'), null, { timeout: 15000 }).catch(() => falhas.push(arq));
    // Algumas visões (kanban, analytics) são montadas ao abrir a aba: abre todas antes de gravar.
    await pg.evaluate(async () => {
      const inicial = document.querySelector('[data-model-tab].is-active, [data-model-tab][aria-selected="true"]');
      for (const t of ['kpi', 'table', 'cards', 'kanban', 'analytics']) {
        TTSCModelKit.switchTab(t);
        await new Promise(r => setTimeout(r, 350));
      }
      TTSCModelKit.switchTab(inicial ? inicial.getAttribute('data-model-tab') : 'table');
      await new Promise(r => setTimeout(r, 200));
    });
    const miolo = await pg.evaluate(() => document.getElementById('model-page').outerHTML);
    const cabeca = src.match(/<head>[\s\S]*?<\/head>/)[0].replace(/<script>[\s\S]*?<\/script>/g, '');
    const rodape = (src.match(/<p class="pg-fonte">[\s\S]*?<\/p>/) || [''])[0];
    const novo = `<!doctype html>\n<html lang="pt-BR" data-theme="light">\n${cabeca}\n<body>\n<main id="main-viewport" class="bg-slate-50" style="padding:14px 16px 24px">\n${miolo}\n${rodape}\n</main>\n</body>\n</html>\n`;
    fs.writeFileSync(arq, novo, 'utf8');
    feitas++;
  }
  console.log('pré-renderizadas', feitas, '| falhas', falhas.length);
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
