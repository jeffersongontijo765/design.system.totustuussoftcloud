// node shoot.js <baseUrl> <outdir> comp1 comp2 ...
const { chromium } = require('playwright');
(async () => {
  const [base, out, ...comps] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 960, height: 600 } });
  const report = {};
  for (const c of comps) {
    for (const th of ['light', 'dark']) {
      const errs = [];
      const onErr = e => errs.push(String(e.message || e));
      const onCon = m => { if (m.type() === 'error') errs.push('console: ' + m.text()); };
      const onFail = r => errs.push('404/fail: ' + r.url());
      p.on('pageerror', onErr); p.on('console', onCon); p.on('requestfailed', onFail);
      const onResp = r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); };
      p.on('response', onResp);
      await p.goto(`${base}/components/${c}/__frame_${th}.html`, { waitUntil: 'load' }).catch(e => errs.push('goto ' + e.message));
      await p.waitForTimeout(700);
      const h = await p.evaluate(() => document.body.scrollHeight);
      const txt = await p.evaluate(() => document.body.innerText.trim().length);
      await p.screenshot({ path: `${out}/${c}-${th}.png`, fullPage: true });
      p.off('pageerror', onErr); p.off('console', onCon); p.off('requestfailed', onFail); p.off('response', onResp);
      report[c + ':' + th] = { h, txt, errs: errs.filter(e => !/fonts\.(googleapis|gstatic)/.test(e)) };
    }
  }
  console.log(JSON.stringify(report, null, 1));
  await b.close();
})();
