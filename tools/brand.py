from PIL import Image, ImageDraw
L=Image.open('/workspace/saintpw/web/w_saintpng.png').convert('RGBA')  # their own logo, from saintpressurewashing.com
bb=L.getbbox(); L=L.crop(bb)
def save(im,w,name,fmt='WEBP'):
    im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    if fmt=='WEBP': im.save('brand/'+name+'.webp','WEBP',quality=90,method=6)
    else: im.save('brand/'+name+'.png',optimize=True)
    print(name, im.size)
save(L,240,'logo-badge-240'); save(L,520,'logo-badge-520'); save(L,1200,'logo-badge-1200','PNG')
# emblem: dog head crop (in 800px view coords x120-300,y165-575 -> scale 3.2)
s=L.width/800
d=L.crop((int(118*s),int(160*s),int(312*s),int(470*s)))
for size in [16,32,48,180,192,512]:
    c=Image.new('RGBA',(size,size),(0,0,0,0)); m=Image.new('L',(size,size),0); ImageDraw.Draw(m).ellipse((0,0,size-1,size-1),fill=255)
    bg=Image.new('RGBA',(size,size),(0,0,0,255)); c.paste(bg,(0,0),m)
    dd=d.copy(); dd.thumbnail((int(size*.80),int(size*.86)),Image.LANCZOS)
    c.alpha_composite(dd,((size-dd.width)//2,int(size*.08)))
    # re-apply circle mask
    c.putalpha(Image.composite(c.getchannel('A'),Image.new('L',(size,size),0),m))
    c.save(f'brand/favicon-{size}.png')
Image.open('brand/favicon-48.png').save('brand/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
