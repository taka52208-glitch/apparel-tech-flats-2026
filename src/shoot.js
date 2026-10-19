const puppeteer = require('puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: process.env.CHROME, headless: true, args: ['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'], timeout: 90000 });
  const p = await b.newPage();
  await p.setViewport({ width: 1900, height: 1320, deviceScaleFactor: 1 });
  for (const n of process.argv.slice(2)) {
    await p.goto('file://' + __dirname + '/../sheets/' + n + '.svg', { waitUntil: 'networkidle0' });
    await p.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 400));
    await p.screenshot({ path: __dirname + '/../img/' + n + '.png' });
  }
  await b.close();
})();
