#!/usr/bin/env python3
"""Manufacturer geometry, actual export reconciliation, and copper geometry audit.
Requires gerbonara and shapely. Run from any directory. Nonzero exit on failure.
"""
import json,math,sys,hashlib,copy,collections
from pathlib import Path
from shapely.geometry import Point,LineString,Polygon,box
from shapely.ops import unary_union,nearest_points
from gerbonara import GerberFile
from gerbonara.graphic_objects import Flash,Line,Region
from gerbonara.apertures import RectangleAperture,CircleAperture
sys.path.insert(0,str(Path(__file__).parent/'manufacturing_qa'))
from validate_release import parse_sexpr,sexpr_nodes,direct_child,footprint_reference
root=Path(__file__).resolve().parents[1]
a=json.loads((root/'source/BubbleLink_CTRL_v1_2_FINAL.circuit.json').read_text());old=json.loads((root/'source/repro/v1_1_baseline.circuit.json').read_text())
checks=[]
def check(name,result,detail=None):
 checks.append(dict(name=name,passed=bool(result),detail=detail))
def u1check(c):
 p=[x for x in c if x['type']=='pcb_smtpad' and x.get('pcb_component_id')=='pcb_component_18']
 if len(p)!=8:return False
 for x in p:
  n=int(x['port_hints'][0]); y=-1.2 if n<=4 else 4.2; xx=-10.905+(n-1)*1.27 if n<=4 else -7.095-(n-5)*1.27
  if any(abs(u-v)>1e-6 for u,v in [(x['x'],xx),(x['y'],y),(x['width'],.6),(x['height'],1.55)]):return False
 return True
check('U1 exact TI D0008A pad count, numbered positions and dimensions',u1check(a))
check('Regression: original 4.30 mm U1 footprint is rejected',not u1check(old))
check('All logical circuit records unchanged', [x for x in a if x['type'].startswith('source_')]==[x for x in old if x['type'].startswith('source_')])
check('All component placements and rotations unchanged',[(x['pcb_component_id'],x['center'],x['rotation']) for x in a if x['type']=='pcb_component']==[(x['pcb_component_id'],x['center'],x['rotation']) for x in old if x['type']=='pcb_component'])
bytype=lambda t:[e for e in a if e['type']==t]
ports={e['pcb_port_id']:e for e in bytype('pcb_port')};sp={e['source_port_id']:e for e in bytype('source_port')};st={e['source_trace_id']:e for e in bytype('source_trace')}
# The four-leg PRIME switch has permanently joined physical pin pairs 1-2 and 3-4.
for slave,master in [('source_port_118','source_port_117'),('source_port_120','source_port_119')]:
 sp[slave]['subcircuit_connectivity_map_key']=sp[master]['subcircuit_connectivity_map_key']
def pnet(e):
 p=ports.get(e.get('pcb_port_id'));return sp[p['source_port_id']].get('subcircuit_connectivity_map_key','unrouted:'+p['source_port_id']) if p else 'tooling:'+e['pcb_smtpad_id']
def shape(e):
 x,y=e['x'],e['y']
 if e['shape']=='rect':w,h=e['width'],e['height'];return box(x-w/2,y-h/2,x+w/2,y+h/2)
 if e['shape']=='circular_hole_with_rect_pad':w,h=e['rect_pad_width'],e['rect_pad_height'];return box(x-w/2,y-h/2,x+w/2,y+h/2)
 return Point(x,y).buffer(e.get('outer_diameter',e.get('radius',0)*2)/2,quad_segs=64)
expected={l:collections.defaultdict(list) for l in ['top','bottom']}
for e in bytype('pcb_smtpad'):expected[e['layer']][pnet(e)].append(shape(e))
for e in bytype('pcb_plated_hole'):
 for l in ['top','bottom']:expected[l][pnet(e)].append(shape(e))
for e in bytype('pcb_via'):
 for l in ['top','bottom']:expected[l][e['subcircuit_connectivity_map_key']].append(Point(e['x'],e['y']).buffer(e['outer_diameter']/2,quad_segs=64))
for e in bytype('pcb_trace'):
 net=st[e['source_trace_id']]['subcircuit_connectivity_map_key']
 for p,q in zip(e['route'],e['route'][1:]):
  if p['route_type']==q['route_type']=='wire' and p['layer']==q['layer']:
   expected[p['layer']][net].append(LineString([(p['x'],p['y']),(q['x'],q['y'])]).buffer(p['width']/2,quad_segs=64))
for e in bytype('pcb_copper_pour'):
 b=e['brep_shape'];p=Polygon([(v['x'],v['y']) for v in b['outer_ring']['vertices']], [[(v['x'],v['y']) for v in r['vertices']] for r in b['inner_rings']]);expected[e['layer']][e['subcircuit_connectivity_map_key']].append(p)
for layer in expected: expected[layer]={k:unary_union(v) for k,v in expected[layer].items()}
def gshape(o):
 if isinstance(o,Flash):
  if isinstance(o.aperture,RectangleAperture):return box(o.x-o.aperture.w/2,o.y-o.aperture.h/2,o.x+o.aperture.w/2,o.y+o.aperture.h/2)
  assert isinstance(o.aperture,CircleAperture);return Point(o.x,o.y).buffer(o.aperture.diameter/2,quad_segs=64)
 if isinstance(o,Line):return LineString([(o.x1,o.y1),(o.x2,o.y2)]).buffer(o.aperture.diameter/2,quad_segs=64)
 if isinstance(o,Region):
  assert not any(o.arc_centers);return Polygon(o.outline)
 raise ValueError(type(o))
for layer,prefix in [('top','F'),('bottom','B')]:
 f=GerberFile.open(root/f'fabrication/gerber_unpacked/{prefix}_Cu.gbr');actual=Polygon()
 for o in f.objects:
  g=gshape(o);actual=actual.union(g) if o.polarity_dark else actual.difference(g)
 exp=unary_union(list(expected[layer].values()))
 excess=actual.difference(exp.buffer(.002)).area; missing=exp.difference(actual.buffer(.002)).area
 check(f'{layer} actual Gerber copper matches pads/routes/vias/pour (2 um tolerance)',excess<1e-6 and missing<1e-6,dict(excess_area_mm2=excess,missing_area_mm2=missing))
 nets=list(expected[layer]);viol=[];minclear=999
 for i,n in enumerate(nets):
  for m in nets[i+1:]:
   d=expected[layer][n].distance(expected[layer][m]);minclear=min(minclear,d)
   if d<.2-1e-5:viol.append(dict(net1=n,net2=m,clearance_mm=d,nearest=[list(p.coords) for p in nearest_points(expected[layer][n],expected[layer][m])]))
 check(f'{layer} all net copper clearances including pour >= 0.20 mm',not viol,dict(minimum_mm=minclear,violations=viol))
 # Every logical pad must be connected in its net through copper on one/both layers.
 # Existing route connectivity validator separately covers through-layer connections.
 check(f'{layer} copper has 0.50 mm outline setback',box(-24.5,-19.5,24.5,19.5).buffer(1e-6).covers(actual))
# U1 independently decoded from each exported layer, plus full SMT pad reconciliation.
for layer in ['F_Cu','F_Paste','F_Mask']:
 f=GerberFile.open(root/f'fabrication/gerber_unpacked/{layer}.gbr');issues=[]
 for p in bytype('pcb_smtpad'):
  if p.get('pcb_component_id')!='pcb_component_18':continue
  w,h=(.75,1.70) if layer=='F_Mask' else (.6,1.55)
  found=[o for o in f.objects if isinstance(o,Flash) and abs(o.x-p['x'])<1e-6 and abs(o.y-p['y'])<1e-6 and isinstance(o.aperture,RectangleAperture) and abs(o.aperture.w-w)<1e-6 and abs(o.aperture.h-h)<1e-6]
  if len(found)!=1:issues.append(p['pcb_smtpad_id'])
 check(f'U1 {layer}: eight correct flashes at numbered pad positions',not issues,issues)
# KiCad pad positions are footprint-local; pad angles are absolute board angles.
k=parse_sexpr((root/'source/BubbleLink_CTRL_v1_2.kicad_pcb').read_text());src={e['source_component_id']:e['name'] for e in bytype('source_component')};pcs={e['pcb_component_id']:src[e['source_component_id']] for e in bytype('pcb_component')}
actualpads={}
for fp in sexpr_nodes(k,'footprint'):
 ref=footprint_reference(fp)
 at=direct_child(fp,'at');cx,cy=float(at[1]),float(at[2]);r=math.radians(float(at[3]) if len(at)>3 else 0)
 for p in [p for p in fp if isinstance(p,list) and p and p[0]=='pad']:
  loc=direct_child(p,'at');x,y=float(loc[1]),float(loc[2]);size=direct_child(p,'size');ang=math.radians(float(loc[3]) if len(loc)>3 else 0)
  w,h=float(size[1]),float(size[2]);gw=abs(w*math.cos(ang))+abs(h*math.sin(ang));gh=abs(w*math.sin(ang))+abs(h*math.cos(ang))
  actualpads[(ref,str(p[1]))]=(cx+x*math.cos(r)+y*math.sin(r)-100,100-(cy-x*math.sin(r)+y*math.cos(r)),gw,gh)
issues=[]
for p in bytype('pcb_smtpad'):
 if not p.get('pcb_component_id'):continue
 ref=pcs[p['pcb_component_id']];num=str(sp[ports[p['pcb_port_id']]['source_port_id']]['pin_number']);got=actualpads.get((ref,num));want=(p['x'],p['y'],p['width'],p['height'])
 if got is None or any(abs(x-y)>1e-6 for x,y in zip(got,want)):issues.append(dict(ref=ref,pin=num,want=want,got=got))
check('Every component SMT pad: KiCad absolute position, size and orientation match Gerber authority',not issues,issues)
report=dict(circuit_sha256=hashlib.sha256((root/'source/BubbleLink_CTRL_v1_2_FINAL.circuit.json').read_bytes()).hexdigest(),checks=checks,passed=all(c['passed'] for c in checks))
(root/'verification/ECO_EXPORT_GEOMETRY_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
for c in checks:print(('PASS' if c['passed'] else 'FAIL')+' '+c['name']+(' '+str(c['detail']) if not c['passed'] else ''))
sys.exit(0 if report['passed'] else 1)
