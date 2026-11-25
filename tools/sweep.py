# Align FB before/after pairs (ECC homography on edge maps), remove their corner watermark by inpainting, crop 16:9
import cv2,numpy as np
P='/workspace/saintpw/photos/'; O='/workspace/saintpw/site-src/img/'
def wm_mask(B,scale=1.2):
    g=cv2.cvtColor(B,cv2.COLOR_BGR2GRAY); h,w=g.shape
    sub=(g[:150,w-170:]<35).astype(np.uint8); ys,xs=np.nonzero(sub); cx=xs.mean()+w-170; cy=ys.mean(); r=np.sqrt(len(xs)/np.pi)
    m=np.zeros((h,w),np.uint8); cv2.circle(m,(int(cx),int(cy)),int(r*scale)+5,255,-1); return m
def edges(g):
    g=cv2.GaussianBlur(g,(5,5),0).astype(np.float32); return np.sqrt(cv2.Sobel(g,cv2.CV_32F,1,0)**2+cv2.Sobel(g,cv2.CV_32F,0,1)**2)
# crop boxes (x,y,w,h) chosen inside the valid warp area and left of the corner watermark
CROP={'sweep-lot':(42,27,396,264),'sweep-annex':(55,40,393,262)}
def go(a,b,H0,out):
    A=cv2.imread(P+a+'.jpg');B=cv2.imread(P+b+'.jpg')
    ea=edges(cv2.cvtColor(A,cv2.COLOR_BGR2GRAY));eb=edges(cv2.cvtColor(B,cv2.COLOR_BGR2GRAY))
    mk=np.full(eb.shape,255,np.uint8);mk[0:140,410:]=0
    W=np.linalg.inv(H0).astype(np.float32)
    cc,W=cv2.findTransformECC(eb,ea,W,cv2.MOTION_HOMOGRAPHY,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,400,1e-6),mk,5)
    sz=(B.shape[1],B.shape[0]); fl=cv2.INTER_CUBIC+cv2.WARP_INVERSE_MAP
    w=cv2.warpPerspective(A,W,sz,flags=fl,borderMode=cv2.BORDER_REPLICATE)
    valid=cv2.warpPerspective(np.full(A.shape[:2],255,np.uint8),W,sz,flags=cv2.WARP_INVERSE_MAP)>250
    l2,t2,tw,th=CROP[out]
    assert valid[t2:t2+th,l2:l2+tw].all(), out
    for im,n in [(w,'before'),(B,'after')]:
        c=im[t2:t2+th,l2:l2+tw]
        cv2.imwrite(f'{O}{out}-{n}.webp',c,[cv2.IMWRITE_WEBP_QUALITY,90])
    cv2.imwrite(f'/workspace/saintpw/chk_{out}.jpg',np.hstack([w[t2:t2+th,l2:l2+tw],B[t2:t2+th,l2:l2+tw]]))
    print(out,cc,tw,th)
pa=np.float32([[267,67],[405,221],[518,225],[225,294],[179,71]]);pb=np.float32([[263,69],[361,213],[487,230],[165,282],[184,78]])
go('f11','f12',cv2.findHomography(pa,pb,0)[0],'sweep-lot')
go('f13','f14',np.array([[.901,.046,42.4],[-.046,.901,51.2],[0,0,1]]),'sweep-annex')
