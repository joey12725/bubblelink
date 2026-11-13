from pathlib import Path
import json,csv
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
from reportlab.lib.colors import HexColor,Color,white,black
root=Path(__file__).resolve().parents[2]
a=json.loads((root/'source/BubbleLink_CTRL_v1_2_FINAL.circuit.json').read_text());src={e['source_component_id']:e for e in a if e['type']=='source_component'};pcs={e['pcb_component_id']:e for e in a if e['type']=='pcb_component'};ports={e['pcb_port_id']:e for e in a if e['type']=='pcb_port'};sp={e['source_port_id']:e for e in a if e['type']=='source_port'}
pads=[e for e in a if e['type'] in ['pcb_smtpad','pcb_plated_hole']]
def ref(p):return src[pcs[p['pcb_component_id']]['source_component_id']]['name'] if p.get('pcb_component_id') else 'FID'
def num(p):return str(sp[ports[p['pcb_port_id']]['source_port_id']]['pin_number']) if p.get('pcb_port_id') else ''
W,H=595.276,841.89;c=canvas.Canvas(str(root/'drawings/BubbleLink_CTRL_v1_2_Assembly_and_U1_Detail.pdf'),pagesize=(W,H));c.setTitle('BubbleLink CTRL v1.2 - assembly and U1 land pattern')
navy=HexColor('#13354B');blue=HexColor('#217BA2');orange=HexColor('#D26628');gray=HexColor('#8C9499')
def text(x,y,s,size=10,color=navy):c.setFillColor(color);c.setFont('DejaVu',size);c.drawString(x,y,s)
def header(title,sub):
 text(38,797,'BUBBLELINK / CTRL v1.2',12,blue);text(38,771,title,21);text(38,749,sub,9)
def footer(page):
 text(38,29,'ECO 2026-09-09  |  Dimensions in mm  |  Top view',8,gray);text(536,29,str(page),8,gray)
header('Assembly and polarity reference','41 top-side SMT placements. THT, test points, mounting holes and DNP parts are not assembly items.')
ox,oy,scale=72,334,9
# Final board outline and all physical lands, no inferred pin-1 corner flags.
c.setLineWidth(.8);c.setStrokeColor(navy);c.rect(ox,oy,450,360)
for e in a:
 if e['type']=='pcb_hole':
  c.setFillColor(HexColor('#E6EAED'));c.circle(ox+(e['x']+25)*scale,oy+(e['y']+20)*scale,e['hole_diameter']/2*scale,fill=1,stroke=0)
for p in pads:
 x=ox+(p['x']+25)*scale;y=oy+(p['y']+20)*scale;rr=ref(p);nn=num(p)
 if p['type']=='pcb_smtpad':
  c.setFillColor(orange if nn=='1' and rr in ['U1','U2','Q1','Q2','Q3','D1'] else (HexColor('#D6EAF3') if rr!='R22' else HexColor('#ECEEEF')))
  c.setStrokeColor(blue if rr!='R22' else gray);c.setLineWidth(.4)
  if p['shape']=='rect':c.rect(x-p['width']*scale/2,y-p['height']*scale/2,p['width']*scale,p['height']*scale,fill=1)
  else:c.circle(x,y,p['radius']*scale,fill=1)
 else:
  r=p.get('outer_diameter',p.get('rect_pad_width',1.7))/2*scale;c.setStrokeColor(gray);c.setFillColor(white);c.circle(x,y,r,fill=1);c.circle(x,y,p['hole_diameter']/2*scale)
for pc in pcs.values():
 rr=src[pc['source_component_id']]['name']
 if rr.startswith('H'):continue
 x=ox+(pc['center']['x']+25)*scale;y=oy+(pc['center']['y']+20)*scale
 c.setFillColor(navy if rr not in ['R22','J4'] else gray);c.setFont('DejaVu-Bold' if rr in ['U1','U2','Q1','Q2','Q3','D1'] else 'DejaVu',6.5)
 c.drawCentredString(x,y-2,rr)
# Explicit U1 body & notch; pin 1 lower-left in this released top-view orientation.
c.setStrokeColor(navy);c.setLineWidth(.6);c.rect(ox+13.55*scale,oy+(21.5-1.955)*scale,4.9*scale,3.91*scale)
text(72,711,'BOARD TOP  /  50 x 40 mm',10)
text(73,315,'Orange land = physical pad 1 for U1, U2, Q1-Q3 and D1.',9,orange)
text(73,299,'D1 pad 1 is cathode: align the package band with the orange land.',9)
text(73,282,'Datum: lower-left corner. +X right, +Y up. Do not mirror.',9)
text(38,252,'Critical orientation checks',12)
rows=[('U1','Pin 1 OUT1','14.095','18.800'),('U2','Pin 1 GND','34.638','20.050'),('Q1','Pin 1 gate','22.550','23.363'),('Q2','Pin 1 gate','36.138','9.050'),('Q3','Pin 1 gate','23.863','13.950'),('D1','Pad 1 cathode / band','40.500','7.800')]
# Derive every position from serialized pads; never from manually entered angles.
rows=[]
for rr,desc in [('U1','OUT1'),('U2','GND'),('Q1','Gate'),('Q2','Gate'),('Q3','Gate'),('D1','Cathode / band')]:
 p=next(p for p in pads if ref(p)==rr and num(p)=='1');rows.append((rr,desc,f"{p['x']+25:.4f}",f"{p['y']+20:.4f}"))
for i,row in enumerate([('Ref','Pad 1 function','X (mm)','Y (mm)')]+rows):
 y=231-i*18
 if i==0:c.setFillColor(HexColor('#E8F1F5'));c.rect(38,y-5,519,18,fill=1,stroke=0)
 for x,s in zip([45,120,369,470],row):text(x,y,s,9)
text(38,86,'J4 and R22: DNP. Fit C9 and R18. No through-hole or bottom assembly.',9)
text(38,70,'Use the supplied BOM, CPL and assembly notes. Numeric rotations alone are insufficient.',9)
footer(1);c.showPage()
header('U1 / TI D0008A land pattern','Keep Texas Instruments TLV1822QDRQ1. This revision corrects the PCB footprint; no electrical substitution.')
cx,cy,s=265,536,37
up=sorted([p for p in pads if ref(p)=='U1'],key=lambda p:int(num(p)))
for p in up:
 x=cx+(p['x']+9)*s;y=cy+(p['y']-1.5)*s
 c.setFillColor(HexColor('#E0E7EA'));c.rect(x-.75*s/2,y-1.70*s/2,.75*s,1.70*s,fill=1,stroke=0)
 c.setFillColor(orange if num(p)=='1' else blue);c.rect(x-.6*s/2,y-1.55*s/2,.6*s,1.55*s,fill=1,stroke=0)
 text(x-3,y+(38 if int(num(p))>=5 else -46),num(p),11,navy)
c.setStrokeColor(gray);c.setDash(3,2);c.rect(cx-4.9/2*s,cy-3.91/2*s,4.9*s,3.91*s);c.setDash()
text(cx-39,cy+5,'BODY OUTLINE',10,gray);text(cx-55,cy-12,'Pin-1 end faces left',10)
def dim(x1,y1,x2,y2,label,tx,ty):
 c.setStrokeColor(navy);c.setLineWidth(.6);c.line(x1,y1,x2,y2)
 if y1==y2:
  for x in [x1,x2]:c.line(x,y1-4,x,y1+4)
 else:
  for y in [y1,y2]:c.line(x1-4,y,x1+4,y)
 text(tx,ty,label,10)
dim(427,cy-2.7*s,427,cy+2.7*s,'5.40 row centers',444,531)
dim(cx-1.905*s,cy+2.7*s+62,cx-.635*s,cy+2.7*s+62,'1.27 pitch',cx-1.9*s,cy+2.7*s+73)
text(38,366,'Copper and paste: 8 x 1.55 across the rows x 0.60 along each row.',10)
text(38,348,'Mask opening: 0.75 x 1.70; 0.075 expansion per side. Non-mask-defined lands.',9)
text(38,330,'Copper inner gap 3.85; outer span 6.95. Lead pitch is 1.27, not 5.40.',9)
text(38,301,'Numbered pad coordinates / finished-board lower-left datum',11)
functions=['OUT1','IN1-','IN1+','V- / GND','IN2+','IN2-','OUT2','V+']
for i,row in enumerate([('Pad','Function','X (mm)','Y (mm)')]+[(num(p),functions[int(num(p))-1],f"{p['x']+25:.4f}",f"{p['y']+20:.4f}") for p in up]):
 y=279-i*18
 if i==0:c.setFillColor(HexColor('#E8F1F5'));c.rect(38,y-5,519,18,fill=1,stroke=0)
 for x,v in zip([45,115,338,450],row):text(x,y,v,9)
text(38,101,'Assembly stencil reference: TI example uses 0.125 mm thickness. PCBWay should',9)
text(38,87,'confirm its process choice and paste release for the complete SMT population.',9)
text(38,65,'Source: TI D0008A, drawing 4214825/C, board-layout and stencil examples.',8,gray)
footer(2);c.save()
with (root/'assembly/CRITICAL_PAD1_COORDINATES.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Reference','Pad 1 function','X mm lower-left datum','Y mm lower-left datum']);w.writerows(rows)
