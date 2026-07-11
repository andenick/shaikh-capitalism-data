import re, os, json
ROOT='Technical'
full=json.load(open(f'{ROOT}/MIGRATION/KB_FIGURE_INDEX_full.json',encoding='utf-8'))
idx=full['captioned']; KB_CH=set(full['chapters_with_kb'])
KB_KEYS=set(idx.keys())
# build base-existence: a figure "N.M" exists if "N.M" or "N.MA/B/.." captioned
base_exist=set()
for k in KB_KEYS:
    base_exist.add(k)
    mm=re.match(r'(\d+)\.(\d+)',k)
    if mm: base_exist.add(f"{mm.group(1)}.{mm.group(2)}")
ref_re=re.compile(r'Fig(?:ure|\.)?\s*(\d+)\.(\d+)([A-Za-z]?)\b')

sd=f'{ROOT}/docs/series'
files=sorted(f for f in os.listdir(sd) if f.endswith('_DPR.md') or f.endswith('_EPR.md'))
total_refs=0; bad=[]
for f in files:
    txt=open(os.path.join(sd,f),encoding='utf-8',errors='replace').read()
    for m in ref_re.finditer(txt):
        maj,mn,suf=m.group(1),m.group(2),m.group(3)
        total_refs+=1
        if int(maj) not in KB_CH:
            continue  # no KB -> cannot verify, skip
        base=f"{maj}.{mn}"; key=f"{maj}.{mn}{suf}"
        if key in base_exist or base in base_exist:
            continue
        i=m.start()
        bad.append((f,f"Fig{maj}.{mn}{suf}",txt[max(0,i-25):i+90].replace('\n',' ').strip()))

print(f"Total figure references scanned across {len(files)} DPR+EPR files: {total_refs}")
print(f"KB-covered chapters: {sorted(KB_CH)}")
print(f"NONEXISTENT figure refs in KB-covered chapters: {len(bad)}")
for f,fig,ctx in bad:
    print(f"  {f}: {fig} | ...{ctx[:80]}...")
print("CONFIRMED CLEAN" if not bad else "STRAYS REMAIN")
