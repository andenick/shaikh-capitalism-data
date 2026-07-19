import re, os, json
ROOT='Technical'
reg=json.load(open(f'{ROOT}/series_registry.json',encoding='utf-8'))['series']
full=json.load(open(f'{ROOT}/MIGRATION/KB_FIGURE_INDEX_full.json',encoding='utf-8'))
idx=full['captioned']; KB_CH=set(full['chapters_with_kb'])
ref_re=re.compile(r'Fig(?:ure|\.)?\s*(\d+)\.(\d+)([A-Za-z]?)\b')

def keyset(figs):
    out=set()
    for f in figs or []:
        m=ref_re.search(f)
        if m: out.add((m.group(1),m.group(2),m.group(3)))
    return out

print("SERIES WHERE A REGISTRY FIGURE IS NOT MENTIONED IN ITS OWN DPR")
print("(potential stray: DPR may cite the wrong number as primary)\n")
flagged=[]
for sid in sorted(reg):
    e=reg[sid]; ch=e.get('chapter')
    reg_keys=keyset(e.get('figures'))
    if not reg_keys: continue
    path=f"{ROOT}/docs/series/{sid}_DPR.md"
    if not os.path.exists(path): continue
    txt=open(path,encoding='utf-8',errors='replace').read()
    dpr_keys={(m.group(1),m.group(2),m.group(3)) for m in ref_re.finditer(txt)}
    missing=reg_keys-dpr_keys
    if missing:
        flagged.append((sid,ch,sorted(f"Fig{a}.{b}{c}" for a,b,c in missing),sorted(f"Fig{a}.{b}{c}" for a,b,c in dpr_keys if int(a)==(ch or 0))))
for sid,ch,miss,dpr_own in flagged:
    kb='KB' if ch in KB_CH else 'noKB'
    print(f"  {sid} ch{ch} [{kb}]: registry fig {miss} NOT in DPR. DPR own-ch refs: {dpr_own}")
print(f"\n  flagged: {len(flagged)}")
