import re, os, json, difflib

ROOT = 'Technical'
idx = json.load(open(f'{ROOT}/MIGRATION/KB_FIGURE_INDEX.json', encoding='utf-8'))
full = json.load(open(f'{ROOT}/MIGRATION/KB_FIGURE_INDEX_full.json', encoding='utf-8'))
reg = json.load(open(f'{ROOT}/series_registry.json', encoding='utf-8'))['series']
KB_CH = set(full['chapters_with_kb'])          # chapters that have an own KB file
KB_KEYS = set(idx.keys())                       # captioned figures present in KB

series_dir = f'{ROOT}/docs/series'

# figure reference regex: captures "Figure 2.1", "Fig2.1", "Fig. 2.1", "Fig 2.1", with optional A/B suffix
ref_re = re.compile(r'Fig(?:ure|\.)?\s*(\d+)\.(\d+)([A-Za-z]?)\b')

def norm(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return ' '.join(s.split())

def fig_exists(maj, mn, suf):
    """Does this figure number exist in the KB for a KB-covered chapter?"""
    if int(maj) not in KB_CH:
        return None  # chapter has no KB -> cannot verify
    base = f"{maj}.{mn}"
    if suf:
        return (base + suf) in KB_KEYS or base in KB_KEYS  # suffix may collapse
    # exists if base captioned, OR any suffixed variant captioned (e.g. 2.4 -> 2.4A)
    if base in KB_KEYS:
        return True
    return any(k == base or k.startswith(base + ('' )) and k[len(base):len(base)+1].isalpha()
               for k in KB_KEYS)

rows = []          # mismatch / finding rows
nonexistent = []   # refs to figures that don't exist for KB-covered chapters

sids = sorted(s for s in reg)
for sid in sids:
    entry = reg[sid]
    reg_figs = entry.get('figures') or []
    reg_fig_keys = set()
    for f in reg_figs:
        m = ref_re.search(f)
        if m:
            reg_fig_keys.add((m.group(1), m.group(2), m.group(3)))
    ch = entry.get('chapter')
    for suffix in ('DPR', 'EPR'):
        path = f'{series_dir}/{sid}_{suffix}.md'
        if not os.path.exists(path):
            continue
        txt = open(path, encoding='utf-8', errors='replace').read()
        seen = set()
        for m in ref_re.finditer(txt):
            maj, mn, suf = m.group(1), m.group(2), m.group(3)
            tup = (maj, mn, suf)
            key = f"{maj}.{mn}{suf}"
            # context window around the ref for caption matching
            i = m.start()
            ctx = txt[max(0, i-20):i+160]
            ex = fig_exists(maj, mn, suf)
            rec = {"sid": sid, "file": suffix, "ref": f"Fig{maj}.{mn}{suf}",
                   "chapter": ch, "ref_chapter": int(maj)}
            if ex is False:
                rec["issue"] = "NONEXISTENT_IN_KB"
                rec["ctx"] = ctx.replace('\n', ' ')
                nonexistent.append(rec)
                rows.append(rec)
            elif ex is None:
                # chapter without KB - only flag if it cites a chapter with no KB at all
                pass
            seen.add(tup)
        # registry-vs-DPR/EPR agreement (only meaningful for DPR which states the canonical fig)
        # flag figures in registry not mentioned in DPR text, and DPR figs not in registry
        if suffix == 'DPR' and reg_fig_keys:
            dpr_keys = {(a, b, c) for (a, b, c) in seen}
            # only count refs whose chapter == series chapter (ignore cross-chapter mentions)
            dpr_own = {(a, b, c) for (a, b, c) in dpr_keys if int(a) == ch}
            reg_own = {(a, b, c) for (a, b, c) in reg_fig_keys if int(a) == ch}
            missing_in_dpr = reg_own - dpr_own
            extra_in_dpr = dpr_own - reg_own
            if missing_in_dpr or extra_in_dpr:
                rows.append({"sid": sid, "file": "DPR", "issue": "REGISTRY_DPR_MISMATCH",
                             "chapter": ch,
                             "registry": sorted(f"Fig{a}.{b}{c}" for a, b, c in reg_own),
                             "dpr_own_chapter_refs": sorted(f"Fig{a}.{b}{c}" for a, b, c in dpr_own),
                             "reg_only": sorted(f"Fig{a}.{b}{c}" for a, b, c in missing_in_dpr),
                             "dpr_only": sorted(f"Fig{a}.{b}{c}" for a, b, c in extra_in_dpr)})

json.dump({"nonexistent": nonexistent, "findings": rows},
          open(f'{ROOT}/MIGRATION/FIGURE_AUDIT_FINDINGS.json', 'w', encoding='utf-8'),
          indent=2, ensure_ascii=False)

print("=== NONEXISTENT FIGURE REFS (KB-covered chapters) ===")
for r in nonexistent:
    print(f"  {r['sid']} {r['file']}: {r['ref']}  | ctx: ...{r['ctx'][:90]}...")
print(f"  count: {len(nonexistent)}")
print()
print("=== REGISTRY vs DPR MISMATCHES ===")
for r in rows:
    if r.get('issue') == 'REGISTRY_DPR_MISMATCH':
        print(f"  {r['sid']} ch{r['chapter']}: registry={r['registry']} reg_only={r['reg_only']} dpr_only={r['dpr_only']}")
print("Findings written to FIGURE_AUDIT_FINDINGS.json")
