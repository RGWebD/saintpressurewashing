import asyncio, json, sys, os
from playwright.async_api import async_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:47290/'
TAG = sys.argv[2] if len(sys.argv) > 2 else 'r1'
OUT = '/workspace/saintpw/qa/shots'
PAGES = ['index.html','services.html','work.html','about.html','contact.html','404.html','nope.html']
async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        report = []
        for w, h in [(1440, 900), (390, 844)]:
            for rm in ['no-preference', 'reduce']:
                ctx = await b.new_context(viewport={'width': w, 'height': h}, reduced_motion=rm, device_scale_factor=1)
                for pg in PAGES:
                    page = await ctx.new_page(); errs = []
                    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
                    page.on('pageerror', lambda e: errs.append(str(e)))
                    await page.goto(BASE + pg, wait_until='load')
                    await page.wait_for_timeout(2400)
                    # scroll through to trigger reveals
                    H = await page.evaluate('document.documentElement.scrollHeight')
                    y = 0
                    while y < H:
                        await page.evaluate(f'window.scrollTo(0,{y})'); await page.wait_for_timeout(120); y += 500
                    await page.wait_for_timeout(2300)
                    r = await page.evaluate('''() => {
                      const o = document.documentElement.scrollWidth - window.innerWidth;
                      const imgs=[...document.images]; const broken = imgs.filter(i=>i.getAttribute('src') && i.complete && i.naturalWidth===0).map(i=>i.src);
                      const srcs = imgs.map(i=>i.getAttribute('src')).filter(s=>s && s.startsWith('img/'));
                      const dup = srcs.filter((s,i)=>srcs.indexOf(s)!==i);
                      const hidden=[...document.querySelectorAll('.rv,.jet,.stall line')].filter(e=>{const cs=getComputedStyle(e);return parseFloat(cs.opacity)<0.99}).length;
                      const counters=[...document.querySelectorAll('[data-count]')].map(e=>[e.textContent, (+e.dataset.count).toFixed(e.dataset.dec|0)]);
                      let ld=[];for(const s of document.querySelectorAll('script[type="application/ld+json"]')){try{ld.push(JSON.parse(s.textContent)['@type'])}catch(e){ld.push('INVALID')}}
                      return {overflow:o, broken, dup, hidden, counters, ld, h:document.documentElement.scrollHeight};
                    }''')
                    if w == 390 and rm == 'no-preference' and pg == 'index.html':
                        await page.evaluate('window.scrollTo(0,0)'); await page.wait_for_timeout(300)
                        await page.click('.burger'); await page.wait_for_timeout(500)
                        r['menu_open'] = await page.evaluate('getComputedStyle(document.querySelector(".mmenu")).visibility')
                        await page.screenshot(path=f'{OUT}/{TAG}_menu_390.png')
                        await page.click('.burger'); await page.wait_for_timeout(400)
                    r.update(page=pg, w=w, rm=rm, errs=errs)
                    report.append(r)
                    if rm == 'no-preference':
                        await page.screenshot(path=f'{OUT}/{TAG}_{pg[:-5]}_{w}_full.png', full_page=True)
                    await page.close()
                await ctx.close()
        await b.close()
        bad = 0
        for r in report:
            issues = []
            if r['overflow'] > 0: issues.append(f"overflow {r['overflow']}")
            if r['broken']: issues.append(f"broken {r['broken']}")
            if r['dup']: issues.append(f"dup {r['dup']}")
            if r['hidden']: issues.append(f"hidden {r['hidden']}")
            if any(a != b for a, b in r['counters']): issues.append(f"counters {r['counters']}")
            if 'INVALID' in r['ld']: issues.append('ld invalid')
            if r['errs']: issues.append(f"errs {r['errs'][:3]}")
            if 'menu_open' in r and r['menu_open'] != 'visible': issues.append('menu fail')
            bad += bool(issues)
            print(f"{r['page']:14} {r['w']} {r['rm']:13} h={r['h']:6} ld={r['ld']} {'OK' if not issues else issues}")
        print('ISSUES' if bad else 'ALL CLEAN')
asyncio.run(run())
