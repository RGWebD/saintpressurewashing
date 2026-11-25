from PIL import Image, ImageFilter
import os
P='/workspace/saintpw/photos/'; W='/workspace/saintpw/web/'; O='img/'
def save(im, name, w, q=80):
    im=im.convert('RGB')
    if im.width>w: im=im.resize((w, round(im.height*w/im.width)), Image.LANCZOS)
    im.save(O+name+'.webp','WEBP',quality=q,method=6); print(name, im.size)
def blur(im, box, r=10):
    reg=im.crop(box).filter(ImageFilter.GaussianBlur(r)); im.paste(reg, box[:2]); return im
h=Image.open(W+'w_GENB1789.JPEG'); save(h,'hero-lot',2200,74); save(h,'hero-lot-m',1100,76)
save(Image.open(W+'w_blob.png'),'ada-stripes',1600)
save(Image.open(W+'w_RUBI8550.JPEG'),'residential-drive',1600)
save(Image.open(W+'w_IMG_1206.JPG'),'warehouse-midwash',1100)
for f in ['f01','f02','f03','f04','f05','f06','f07','f08','f09','f10','f11','f12','f13','f14','f16','f17','f19']:
    save(Image.open(P+f+'.jpg'), f, 590, 84)
im=Image.open(P+'f18.jpg').convert('RGB'); im=blur(im,(440,0,590,30),8); save(im,'f18',590,84)
save(Image.open(P+'cover.jpg'),'rig-night',960,82)
