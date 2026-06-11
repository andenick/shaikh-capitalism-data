"""Concatenate per-chapter research summaries into a single narrative."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# Parameterized 2026-05-19 per Decision 0006: derive paths from script location
# (scripts/ -> replicator/ -> Technical/) with RSCD_TECHNICAL env override.
_SCRIPT_DIR = Path(__file__).resolve().parent
_TECHNICAL_DEFAULT = _SCRIPT_DIR.parents[1]  # replicator/scripts -> Technical
TECHNICAL = Path(os.environ.get("RSCD_TECHNICAL", str(_TECHNICAL_DEFAULT)))
SUMM_DIR = TECHNICAL / "docs" / "chapters"


def main(out_path: str) -> None:
    reg = json.loads((TECHNICAL / "series_registry.json").read_text(encoding="utf-8"))
    series = reg.get("series", {})
    by_ch: dict[int, list[str]] = {}
    for sid, m in series.items():
        ch = m.get("chapter")
        if isinstance(ch, int) or (isinstance(ch, str) and ch.isdigit()):
            ch = int(ch)
            by_ch.setdefault(ch, []).append(sid)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        fh.write("# RSCD v1.0 — Per-Chapter Narrative\n\n")
        fh.write("Chapter-by-chapter walkthrough of every series authored in this release.\n\n")
        fh.write("---\n\n")

        for ch in sorted(by_ch.keys()):
            sids = sorted(by_ch[ch])
            fh.write(f"## Chapter {ch}\n\n")
            fh.write(f"**Series in this chapter**: {len(sids)} — {', '.join(sids)}\n\n")
            # Try to include the chapter research summary
            cand = SUMM_DIR / f"CH{ch}_RESEARCH_SUMMARY.md"
            if cand.exists():
                txt = cand.read_text(encoding="utf-8")
                # Strip top-level headings, demote them
                txt = re.sub(r"^# ", "### ", txt, flags=re.MULTILINE)
                txt = re.sub(r"^## ", "#### ", txt, flags=re.MULTILINE)
                fh.write(txt)
                fh.write("\n\n")
            else:
                # Per-series mini-table
                fh.write("| SID | Name | Figures | Year range (extended) | Status |\n")
                fh.write("|-----|------|---------|----------------------|--------|\n")
                for sid in sids:
                    s = series[sid]
                    figs = s.get("figures") or []
                    figs_s = ", ".join(str(f) for f in figs) if isinstance(figs, list) else str(figs)
                    yr = s.get("year_range_extension") or s.get("year_range") or []
                    yr_s = f"{yr[0]}-{yr[1]}" if isinstance(yr, list) and len(yr) == 2 else ""
                    fh.write(f"| {sid} | {s.get('name', '')} | {figs_s} | {yr_s} | {s.get('status', '')} |\n")
                fh.write("\n")
            fh.write("---\n\n")

        # External + analytical
        es_sids = sorted([sid for sid in series if sid.startswith("ES")])
        as_sids = sorted([sid for sid in series if sid.startswith("AS")])
        if es_sids:
            fh.write("## External Studies (ES)\n\n")
            fh.write(f"**Series**: {len(es_sids)} — {', '.join(es_sids)}\n\n")
            fh.write("Replications of econometric studies cited by Shaikh that warrant standalone treatment "
                     "(Shaikh 2020 macro identity; Coronado-Shaikh-Tonak 2020 Mexico; Shaikh-Jacobo 2020 GDP "
                     "decomposition; Weber-Shaikh 2020 China; original Shaikh-Tonak 1986 US profit rate).\n\n")
            for sid in es_sids:
                s = series[sid]
                fh.write(f"- **{sid}** — {s.get('name', '')} ({s.get('status', '')})\n")
            fh.write("\n---\n\n")
        if as_sids:
            fh.write("## Analytical Series (AS)\n\n")
            fh.write(f"**Series**: {len(as_sids)} — {', '.join(as_sids)}\n\n")
            fh.write("Framework-derived series not directly tied to a single book figure: Ch6 GPIM variants "
                     "(general profit rate of integrated capital, multiple specifications) and related "
                     "constructions.\n\n")
            for sid in as_sids:
                s = series[sid]
                fh.write(f"- **{sid}** — {s.get('name', '')} ({s.get('status', '')})\n")
            fh.write("\n")

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    # Parameterized 2026-05-19 per Decision 0006: default out derives from RSCD root.
    _RSCD_ROOT = TECHNICAL.parent  # Technical -> RSCD
    _DEFAULT_OUT = (
        _RSCD_ROOT
        / "Outputs" / "Drive" / "RSCD_v1.0" / "Documentation" / "PER_CHAPTER_NARRATIVE.md"
    )
    out = sys.argv[1] if len(sys.argv) > 1 else str(_DEFAULT_OUT)
    main(out)
