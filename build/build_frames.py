# Harness only: compiles tokens.css and wraps each preview.html like the artifact's preview frame.
import json,os,sys,re
P=sys.argv[1]; OUT=os.path.join(P,'__h'); os.makedirs(OUT,exist_ok=True)
t=json.load(open(os.path.join(P,'tokens.json')))
themes=[x['id'] for x in t['color']['themes']]
def val(tok,th):
    v=tok['value']
    if isinstance(v,str): return v if th==themes[0] else None
    return v.get(th)
css=[]
for th in themes:
    sel=':root, [data-theme="%s"]'%th if th==themes[0] else '[data-theme="%s"]'%th
    lines=[]
    for tok in t['color']['tokens']:
        v=val(tok,th)
        if v: lines.append('--%s:%s;'%(tok['name'],v))
    if th==themes[0]:
        for tok in t.get('shadow',{}).get('tokens',[]): lines.append('--%s:%s;'%(tok['name'],tok['value']))
    css.append(sel+'{'+''.join(lines)+'}')
lines=[]
for fam,d in t.items():
    if fam in('color','type','shadow','name','version','meta'): continue
    for tok in d['tokens']: lines.append('--%s:%s;'%(tok['name'],tok['value']))
for k,v in t['type']['families'].items(): lines.append('--font-%s:%s;'%(k,v))
css.append(':root{'+''.join(lines)+'}')
for f in t['type']['fonts']:
    css.append('@font-face{font-family:"%s";src:url(../fonts/%s);font-weight:%s}'%(f['family'],os.path.basename(f['file']),f['weight']))
open(os.path.join(P,'components','__tokens.css'),'w').write('\n'.join(css))
comps=[d for d in sorted(os.listdir(os.path.join(P,'components'))) if os.path.isfile(os.path.join(P,'components',d,'preview.html'))]
only=sys.argv[2:] 
for c in comps:
    if only and c not in only: continue
    src=open(os.path.join(P,'components',c,'preview.html')).read()
    for th in themes:
        head='<link rel="stylesheet" href="../__tokens.css"><link rel="stylesheet" href="../bundle.css"><script src="../bundle.js"></script>'
        if re.search(r'<head[^>]*>',src): doc=re.sub(r'(<head[^>]*>)',r'\1'+head,src,1)
        else: doc='<!doctype html><html><head>'+head+'</head><body>'+src+'</body></html>'
        doc=re.sub(r'<html([^>]*)>',lambda m:'<html'+re.sub(r'\sdata-theme="[^"]*"','',m.group(1))+' data-theme="%s">'%th,doc,1)
        open(os.path.join(P,'components',c,'__frame_%s.html'%th),'w').write(doc)
print(len(comps))
