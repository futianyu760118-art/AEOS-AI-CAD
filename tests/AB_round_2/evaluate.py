#!/usr/bin/env python3
"""RUGGED-H6000 front-view image quality gate.

Scores reference versus an independently rendered image. It is not a
manufacturing-grade CAD verification and does not guarantee 3D fidelity.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw

ROI_MAIN=(300,330,950,850)
ROI_LEFT=(329,355,434,794)
ROI_RIGHT=(816,355,920,794)
ROI_REFLECTOR=(401,405,854,746)
ROI_LED=(479,475,777,674)

def mask_orange(bgr):
    hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv,np.array([3,125,110]),np.array([23,255,255]))>0

def mask_yellow(bgr):
    hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv,np.array([19,80,145]),np.array([40,255,255]))>0

def roi_boolean(shape,bounds):
    x0,y0,x1,y1=bounds
    a=np.zeros(shape,dtype=bool); a[y0:y1,x0:x1]=True
    return a

def iou(a,b):
    aa=np.count_nonzero(a & b); uni=np.count_nonzero(a | b)
    return round(float(aa/uni),4) if uni else None

def ssim_gray(r,c,bounds):
    x0,y0,x1,y1=bounds
    a=cv2.cvtColor(r[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32)
    b=cv2.cvtColor(c[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32)
    mu1=cv2.GaussianBlur(a,(11,11),1.5); mu2=cv2.GaussianBlur(b,(11,11),1.5)
    va=cv2.GaussianBlur(a*a,(11,11),1.5)-mu1*mu1
    vb=cv2.GaussianBlur(b*b,(11,11),1.5)-mu2*mu2
    cov=cv2.GaussianBlur(a*b,(11,11),1.5)-mu1*mu2
    C1=(.01*255)**2; C2=(.03*255)**2
    s=((2*mu1*mu2+C1)*(2*cov+C2))/((mu1*mu1+mu2*mu2+C1)*(va+vb+C2))
    return round(float(s.mean()),4)

def edge_distance(r,c,bounds):
    x0,y0,x1,y1=bounds
    r=cv2.cvtColor(r[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY)
    c=cv2.cvtColor(c[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY)
    a=cv2.Canny(cv2.GaussianBlur(r,(7,7),2),25,75)>0
    b=cv2.Canny(cv2.GaussianBlur(c,(7,7),2),25,75)>0
    d1=cv2.distanceTransform((~a).astype(np.uint8),cv2.DIST_L2,3)
    d2=cv2.distanceTransform((~b).astype(np.uint8),cv2.DIST_L2,3)
    chamfer=float((d1[b].mean() if b.any() else 500)+(d2[a].mean() if a.any() else 500))/2
    return {'symmetric_chamfer_px':round(chamfer,2),
            'reference_edge_pixels':int(a.sum()),
            'candidate_edge_pixels':int(b.sum())}

def evaluate(reference,candidate,out):
    ref=cv2.imread(str(reference)); can=cv2.imread(str(candidate))
    if ref is None or can is None: raise RuntimeError('Cannot load image')
    if ref.shape!=can.shape:
        raise ValueError(f'Size mismatch {ref.shape} vs {can.shape}: align perspective before scoring')
    h,w=ref.shape[:2]; mask=roi_boolean((h,w),ROI_MAIN)
    ornref=mask_orange(ref)&mask; orncan=mask_orange(can)&mask
    yref=mask_yellow(ref)&roi_boolean((h,w),ROI_LED)
    ycan=mask_yellow(can)&roi_boolean((h,w),ROI_LED)
    report={'reference':str(reference),'candidate':str(candidate),'resolution':[w,h],
      'method':'fixed registration, independent color/edge/photometric comparisons',
      'key_warning':'Color, lighting, rendering and camera differences affect scores; none is CAD geometry accuracy',
      'metrics':{
        'orange_left_iou':iou(ornref&roi_boolean((h,w),ROI_LEFT),orncan&roi_boolean((h,w),ROI_LEFT)),
        'orange_right_iou':iou(ornref&roi_boolean((h,w),ROI_RIGHT),orncan&roi_boolean((h,w),ROI_RIGHT)),
        'led_yellow_region_iou':iou(yref,ycan),
        'main_housing_ssim':ssim_gray(ref,can,ROI_MAIN),
        'reflector_ssim':ssim_gray(ref,can,ROI_REFLECTOR),
        'reflector_edge_distance':edge_distance(ref,can,ROI_REFLECTOR)}}
    Path(out).mkdir(parents=True,exist_ok=True)
    overlay=can.copy()
    ref_only=ornref & ~orncan; can_only=orncan & ~ornref; common=ornref&orncan
    overlay[ref_only]=(30,30,230); overlay[can_only]=(200,160,20); overlay[common]=(70,195,60)
    panels=np.concatenate([ref,can,overlay],axis=1)
    pil=Image.fromarray(cv2.cvtColor(panels,cv2.COLOR_BGR2RGB))
    draw=ImageDraw.Draw(pil)
    for idx,t in enumerate(['REFERENCE','CANDIDATE','ORANGE OVERLAY: GREEN=SHARED RED=REF-ONLY CYAN=CAD-ONLY']):
        x=idx*w+35
        draw.rectangle((x,20,x+min(w-70,830),63),fill=(30,32,37))
        draw.text((x+12,30),t,fill=(255,255,255))
    pil.save(str(Path(out)/'front_comparison.png'),optimize=True)
    x0,y0,x1,y1=ROI_REFLECTOR
    zz=np.concatenate([ref[y0:y1,x0:x1],can[y0:y1,x0:x1]],axis=1)
    cv2.imwrite(str(Path(out)/'reflector_closeup.png'),zz)
    (Path(out)/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--reference',required=True); p.add_argument('--candidate',required=True); p.add_argument('--out',required=True)
    a=p.parse_args()
    print(json.dumps(evaluate(a.reference,a.candidate,a.out),indent=2,ensure_ascii=False))
