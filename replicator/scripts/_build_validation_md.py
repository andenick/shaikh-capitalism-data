"""Render VALIDATION_REPORT.json as a human-readable markdown table."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Parameterized 2026-05-19 per Decision 0006: derive paths from script location
# (scripts/ -> replicator/ -> Technical/) with ARCANUM_ROOT override for portability.
_SCRIPT_DIR = Path(__file__).resolve().parent
_TECHNICAL_DEFAULT = _SCRIPT_DIR.parents[1]  # replicator/scripts -> Technical
TECHNICAL = Path(os.environ.get("RSCD_TECHNICAL", str(_TECHNICAL_DEFAULT)))


def main(out_path: str) -> None:
    rpt = json.loads((TECHNICAL / "VALIDATION_REPORT.json")
                     .read_text(encoding="utf-8"))
    series = rpt.get("series", {})

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        fh.write("# RSCD v1.0 — Validation Report\n\n")
        fh.write(f"Generated: {rpt.get('generated_at', 'unknown')}\n\n")

        from collections import Counter
        c = Counter(s.get("status", "?") for s in series.values())
        fh.write("## Status distribution\n\n")
        fh.write("| Status | Count |\n|--------|-------|\n")
        for k in sorted(c):
            fh.write(f"| {k} | {c[k]} |\n")
        fh.write(f"| **Total** | **{sum(c.values())}** |\n\n")

        fh.write("## Per-series detail\n\n")
        fh.write("| SID | Status | n | MAE | Max abs err | Compare range |\n")
        fh.write("|-----|--------|---|-----|-------------|---------------|\n")
        for sid in sorted(series.keys()):
            s = series[sid]
            n = s.get("n_compared")
            mae = s.get("mae")
            mae_s = "-" if mae is None else f"{mae:.4g}"
            mxa = s.get("max_abs_err")
            mxa_s = "-" if mxa is None else f"{mxa:.4g}"
            rng = s.get("compare_range") or []
            rng_s = f"{rng[0]}-{rng[1]}" if isinstance(rng, list) and len(rng) == 2 else "-"
            n_s = "-" if n is None else str(n)
            fh.write(f"| {sid} | {s.get('status', '?')} | {n_s} | {mae_s} | {mxa_s} | {rng_s} |\n")

    print(f"Wrote {out}")


if __name__ == "__main__":
    # Parameterized 2026-05-19 per Decision 0006: default out_path derives from
    # the RSCD project root (Technical/.. ) with ARCANUM_ROOT override.
    _RSCD_ROOT = TECHNICAL.parent  # Technical -> RSCD
    _DEFAULT_OUT = (
        _RSCD_ROOT
        / "Outputs" / "Drive" / "RSCD_v1.0" / "Documentation" / "VALIDATION_REPORT.md"
    )
    out = sys.argv[1] if len(sys.argv) > 1 else str(_DEFAULT_OUT)
    main(out)
