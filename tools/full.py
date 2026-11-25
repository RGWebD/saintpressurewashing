import asyncio,sys
from playwright.async_api import async_playwright
from PIL import Image
BASE=sys.argv[1]; TAG=sys.argv[2]; pages=sys.argv[3].split(','); widths=[int(x) for x in sys.argv[4].split(',')]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w in widths:
      ctx=await b.new_context(viewport={'width':w,'height':900 if w>800 else 844})
      for pg_ in pages:
        pg=await ctx.new_page(); await pg.goto(BASE+pg_,wait_until='load'); await pg.wait_for_timeout(2500)
        H=await pg.evaluate('document.documentElement.scrollHeight'); y=0
        while y<H: await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(90); y+=450
        await pg.wait_for_timeout(1800); await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(400)
        f=f'/workspace/saintpw/qa/shots/{TAG}_{pg_[:-5]}_{w}_full.png'; await pg.screenshot(path=f,full_page=True)
        im=Image.open(f); 
        # split into chunks for viewing
        ch=2400 if w>800 else 2200; n=0
        for top in range(0,im.height,ch):
          c=im.crop((0,top,im.width,min(im.height,top+ch))); c.thumbnail((900 if w>800 else 390,10000)); c.save(f.replace('_full.png',f'_p{n}.jpg'),quality=80); n+=1
        print(f,im.size,n); await pg.close()
      await ctx.close()
    await b.close()
asyncio.run(m())
