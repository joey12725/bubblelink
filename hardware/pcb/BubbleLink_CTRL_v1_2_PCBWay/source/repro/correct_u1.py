import json,copy,hashlib
from pathlib import Path
baseline=Path(__file__).resolve().parent/'v1_1_baseline.circuit.json'
out=Path(__file__).resolve().parents[2]
a=json.loads(baseline.read_text())
# World coordinates: U1 at (-9,1.5), pins 1-4 on lower row, 8-5 on upper row.
ports={}
for p in a:
 if p['type']=='pcb_smtpad' and p.get('pcb_component_id')=='pcb_component_18':
  old=(p['x'],p['y']); n=int(p['port_hints'][0]); p['y']=-1.2 if n<=4 else 4.2
  p['width']=0.6; p['height']=1.55; p['soldermask_margin']=0.075
  ports[p['pcb_port_id']]=(p['x'],p['y'])
for p in a:
 if p['type']=='pcb_port' and p.get('pcb_port_id') in ports: p['x'],p['y']=ports[p['pcb_port_id']]
 if p['type']=='pcb_solder_paste' and p.get('pcb_component_id')=='pcb_component_18':
  pad=next(x for x in a if x.get('pcb_smtpad_id')==p['pcb_smtpad_id'] and x['type']=='pcb_smtpad')
  p.update(x=pad['x'],y=pad['y'],width=.6,height=1.55)
 if p['type']=='pcb_trace':
  for t in p['route']:
   port=t.get('start_pcb_port_id') or t.get('end_pcb_port_id')
   if port in ports: t['x'],t['y']=ports[port]
 if p['type']=='pcb_component' and p.get('pcb_component_id')=='pcb_component_18': p['width']=4.9;p['height']=6.95
 if p['type']=='pcb_courtyard_outline' and p.get('pcb_component_id')=='pcb_component_18':
  p['outline']=[dict(x=x,y=y) for x,y in [(-11.7,-2.225),(-6.3,-2.225),(-6.3,5.225),(-11.7,5.225)]]
 # Move ground trace around new lower row rather than crossing expanded pads.
 if p['type']=='pcb_trace' and p['source_trace_id']=='source_trace_25':
  pts=[(-7.095,-1.2),(-7.095,-2.4),(-11.55,-2.4),(-11.55,-.75),(-12.2,-.1),(-13,-.1)]
  p['route']=[dict(route_type='wire',x=x,y=y,layer='top',width=.25) for x,y in pts]
  p['route'][0]['start_pcb_port_id']='pcb_port_41';p['route'][-1]['end_pcb_port_id']='pcb_port_47'
 # Keep the TP6 signal via outside U1 pin 8's expanded land.
 if p['type']=='pcb_trace' and p['source_trace_id']=='source_trace_57':
  for t in p['route']:
   if abs(t['x']+10.7)<1e-6 and abs(t['y']-5)<1e-6: t['x']=-10.4;t['y']=5.55
  p['route'].insert(4,dict(route_type='wire',x=-10.4,y=4.65,layer='bottom',width=.25))
  p['route'][5]['x']=-10.95
  p['route'].insert(1,dict(route_type='wire',x=-8.5,y=6.7,layer='top',width=.25))
 if p['type']=='pcb_via' and abs(p['x']+10.7)<1e-6 and abs(p['y']-5)<1e-6: p['x']=-10.4;p['y']=5.55
 # Exit north-row pads vertically before turning across neighboring lands.
 if p['type']=='pcb_trace' and p['source_trace_id'] in ['source_trace_73','source_trace_83']:
  p['route'][1]['y']=4.8
  if p['source_trace_id']=='source_trace_73':
   p['route'][1].update(x=-8.28,y=4.75)
   p['route'][2].update(x=-7.6,y=5.35)
   p['route'][3]['y']=5.35
 # Explicit via-to-pad checks reveal clearances missed by legacy DRC.
 if p['type']=='pcb_trace':
  for t in p['route']:
   if abs(t['x']+9)<1e-6 and abs(t['y']-4.9)<1e-6: t['y']=5.45
   if abs(t['x']+17.7)<1e-6 and abs(t['y']-10.3)<1e-6: t['x']=-17.4;t['y']=10.35
 if p['type']=='pcb_via':
  if p['pcb_via_id']=='pcb_via_search_48': p['y']=5.45
  if p['pcb_via_id']=='pcb_via_search_24': p['x']=-17.4;p['y']=10.35
 if p['type']=='pcb_silkscreen_text' and 'v1.1' in p.get('text',''): p['text']=p['text'].replace('v1.1','v1.2')
# Exact delta/repro baseline retained, no old fabrication zip in the new package.
(out/'source/BubbleLink_CTRL_v1_2_FINAL.circuit.json').write_text(json.dumps(a,indent=2)+'\n')
