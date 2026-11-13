#!/usr/bin/env python3
"""Independent STEP topology/bounds validation via OpenCascade (OCP)."""
import argparse, json
from pathlib import Path
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

def verify(path):
    p=Path(path); rd=STEPControl_Reader()
    status=rd.ReadFile(str(p))
    if status!=IFSelect_RetDone: raise RuntimeError('STEP parse failed')
    n=rd.TransferRoots(); shape=rd.OneShape()
    exp=TopExp_Explorer(shape,TopAbs_SOLID)
    all_solids=0; valid_solids=0; volumes=[]
    while exp.More():
        solid=exp.Current(); all_solids+=1
        if BRepCheck_Analyzer(solid).IsValid(): valid_solids+=1
        props=GProp_GProps(); BRepGProp.VolumeProperties_s(solid,props)
        volumes.append(float(props.Mass())); exp.Next()
    box=Bnd_Box(); BRepBndLib.Add_s(shape,box); lim=box.Get()
    dims=[round(lim[3]-lim[0],2),round(lim[4]-lim[1],2),round(lim[5]-lim[2],2)]
    return {'file':p.name,'read_status':'ok','transferred_roots':n,
      'solids':all_solids,'valid_solids':valid_solids,
      'all_valid':all_solids>0 and all_solids==valid_solids,
      'bbox_xyz_mm':dims,'total_volume_mm3':round(sum(volumes),2),
      'note':'Valid STEP topology does not prove design or dimensional accuracy.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('step'); ap.add_argument('--out')
    args=ap.parse_args(); report=verify(args.step)
    if args.out: Path(args.out).write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
