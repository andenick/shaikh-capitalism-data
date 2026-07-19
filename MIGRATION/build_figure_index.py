import re, os, json
from collections import Counter

kb = 'Inputs/CD2/Inputs/Robert/KB/'
files = sorted(f for f in os.listdir(kb) if re.match(r'ch\d+', f) and f.endswith('.md'))

any_re = re.compile(r'Fig(?:ure|\.)?s?\s+(\d+)\.(\d+)([A-Za-z]?)\b')

def key_of(major, minor, suffix):
    return f"{major}.{minor}" + (suffix if suffix else "")

def sk(k):
    a, b = k.split('.')
    bn = re.match(r'(\d+)([A-Za-z]?)', b)
    return (int(a), int(bn.group(1)), bn.group(2))

# Caption-line patterns, in priority order:
# A) markdown header w/ colon:  ### Figure 10.1: Caption    OR  ### Figures 10.2–10.4: Caption
hdr_re = re.compile(r'^#{1,6}\s*Fig(?:ure|\.)?s?\s+(\d+)\.(\d+)([A-Za-z]?)\s*(?:[–—-]\s*(?:\d+\.)?(\d+)([A-Za-z]?))?\s*:\s*(.+?)\s*$')
# B) standalone caption line: Figure 15.5 Title Words...
cap_re = re.compile(r'^\s*Fig(?:ure|\.)?\s+(\d+)\.(\d+)([A-Za-z]?)\b\s+(.+)$')

index = {}
all_refs = {}

for fn in files:
    ch = re.match(r'ch0?(\d+)', fn).group(1)
    txt = open(os.path.join(kb, fn), encoding='utf-8', errors='replace').read()
    for line in txt.splitlines():
        # A) header style (handles ranges)
        h = hdr_re.match(line)
        if h:
            maj, mn, suf, mn2, suf2, cap = h.groups()
            cap = cap.strip()
            lo = int(mn); hi = int(mn2) if mn2 else lo
            for i in range(lo, hi + 1):
                k = key_of(maj, i, suf if (i == lo) else "")
                prev = index.get(k)
                if prev is None or len(cap) > len(prev):
                    index[k] = cap
            continue
        # B) plain caption line (must look like a title: next word capitalized/number)
        c = cap_re.match(line)
        if c:
            maj, mn, suf, rest = c.groups()
            rest = rest.strip()
            first = rest.split()[0] if rest.split() else ""
            if first[:1].isupper() or first[:1].isdigit():
                k = key_of(maj, mn, suf)
                prev = index.get(k)
                if prev is None or len(rest) > len(prev):
                    index[k] = rest
    # Fallback: prose "Figure N.M <words>" -> short caption if no formal caption found yet
    for m in re.finditer(r'Fig(?:ure|\.)?s?\s+(\d+)\.(\d+)([A-Za-z]?)\s+([a-z][a-z]+\s+(?:[^.]{5,80}))', txt):
        k = key_of(m.group(1), m.group(2), m.group(3))
        if k not in index:
            index[k] = "(prose) " + m.group(4).strip()
    for m in any_re.finditer(txt):
        k = key_of(m.group(1), m.group(2), m.group(3))
        all_refs.setdefault(ch, set()).add(k)
        index.setdefault(k, None)

# actual KB chapters = chapter numbers that have their own file
kb_chapters = sorted(int(re.match(r'ch0?(\d+)', f).group(1)) for f in files)
# drop entries for chapters without an own KB file (cross-ref prose false positives, e.g. 4.5)
for k in list(index):
    if int(k.split('.')[0]) not in kb_chapters:
        del index[k]

clean = {k: index[k] for k in sorted((kk for kk in index if index[kk]), key=sk)}
# existence set (everything referenced anywhere, even uncaptioned)
existence = sorted({k for ch in all_refs for k in all_refs[ch]}, key=sk)

out = 'Technical/MIGRATION/KB_FIGURE_INDEX.json'
json.dump(clean, open(out, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
json.dump({"captioned": clean, "all_referenced": existence,
           "chapters_with_kb": kb_chapters},
          open('Technical/MIGRATION/KB_FIGURE_INDEX_full.json', 'w', encoding='utf-8'),
          indent=2, ensure_ascii=False)

cnt = Counter(int(k.split('.')[0]) for k in clean)
print("=== FIGURE INDEX SIZE PER CHAPTER (captioned) ===")
for ch in sorted(cnt):
    nums = sorted([k for k in clean if int(k.split('.')[0]) == ch], key=sk)
    print(f"  ch{ch:02d}: {cnt[ch]:3d}  range {nums[0]}..{nums[-1]}")
print(f"  TOTAL captioned: {len(clean)}")
print("Chapters with KB (own file):", kb_chapters)
