import re, os, json
ROOT='Technical'
reg=json.load(open(f'{ROOT}/series_registry.json',encoding='utf-8'))['series']
full=json.load(open(f'{ROOT}/MIGRATION/KB_FIGURE_INDEX_full.json',encoding='utf-8'))
idx=full['captioned']; KB_CH=set(full['chapters_with_kb'])
ref_re=re.compile(r'Fig(?:ure|\.)?\s*(\d+)\.(\d+)([A-Za-z]?)\b')

# cases to inspect: SID -> dpr_only figs (own-chapter refs not matching registry)
findings=json.load(open(f'{ROOT}/MIGRATION/FIGURE_AUDIT_FINDINGS.json',encoding='utf-8'))['findings']
cases=[f for f in findings if f.get('issue')=='REGISTRY_DPR_MISMATCH' and f.get('dpr_only')]

for f in cases:
    sid=f['sid']; ch=f['chapter']
    has_kb = ch in KB_CH
    print(f"\n{'='*70}\n{sid}  ch{ch}  KB={'yes' if has_kb else 'NO'}  registry={f['registry']}  dpr_only={f['dpr_only']}")
    path=f"{ROOT}/docs/series/{sid}_DPR.md"
    txt=open(path,encoding='utf-8',errors='replace').read()
    for fig in f['dpr_only']:
        m=re.search(r'Fig(?:ure|\.)?\s*(\d+)\.(\d+)([A-Za-z]?)',fig)
        maj,mn,suf=m.group(1),m.group(2),m.group(3)
        kbkey=f"{maj}.{mn}{suf}"
        kbcap=idx.get(kbkey) or idx.get(f"{maj}.{mn}") or '(no KB caption)'
        regfig=f['registry'][0] if f['registry'] else '?'
        rm=re.search(r'Fig(?:ure|\.)?\s*(\d+)\.(\d+)([A-Za-z]?)',regfig)
        regkey=f"{rm.group(1)}.{rm.group(2)}{rm.group(3)}" if rm else '?'
        regcap=idx.get(regkey) or '(no KB caption)' if has_kb else '(no KB)'
        print(f"  -- DPR cites {fig}: KB caption = {kbcap[:70]}")
        print(f"     registry says {regfig}: KB caption = {str(regcap)[:70]}")
        # show all occurrences of this fig in DPR
        pat=re.compile(re.escape(fig).replace(r'\ ',r'\s*')+r'|'+f'Fig(?:ure|\\.)?\\s*{maj}\\.{mn}{suf}'+r'\b')
        for mm in re.finditer(rf'Fig(?:ure|\.)?\s*{maj}\.{mn}{suf}\b',txt):
            i=mm.start(); print(f"     ctx: ...{txt[max(0,i-30):i+110].strip()}...".replace(chr(10),' '))
