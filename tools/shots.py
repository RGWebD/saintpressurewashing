import asyncio,sys
from playwright.async_api import async_playwright
BASE=sys.argv[1]; TAG=sys.argv[2]; specs=sys.argv[3:]  # page:width:scrollY[:wait]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for s in specs:
      pg_,w,y,*wt=s.split(':'); w=int(w); y=int(y); wt=int(wt[0]) if wt else 3200
      ctx=await b.new_context(viewport={'width':w,'height':900 if w>800 else 844})
      pg=await ctx.new_page(); await pg.goto(BASE+pg_,wait_until='load')
      if y:
        H=await pg.evaluate('document.documentElement.scrollHeight'); yy=0
        while yy<min(y+900,H): await pg.evaluate(f'scrollTo(0,{yy})'); await pg.wait_for_timeout(80); yy+=400
        await pg.evaluate(f'scrollTo(0,{y})')
      await pg.wait_for_timeout(wt)
      ov=await pg.evaluate('document.documentElement.scrollWidth-innerWidth')
      f=f'/workspace/saintpw/qa/shots/{TAG}_{pg_[:-5]}_{w}_{y}.png'; await pg.screenshot(path=f); print(f,'overflow',ov)
      await ctx.close()
    await b.close()
asyncio.run(m())
