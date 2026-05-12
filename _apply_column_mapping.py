"""Update processing modules to use the correct source columns from column_mapping.json."""
import json
import re
from pathlib import Path

with open("config/column_mapping.json", "r") as f:
    mapping = json.load(f)

with open("config/registry.json", "r", encoding="utf-8") as f:
    reg = json.load(f).get("series", {})

with open("config/chapters.json", "r", encoding="utf-8") as f:
    ch_cfg = json.load(f)

for ch_str, ch_info in ch_cfg["chapters"].items():
    ch_num = int(ch_str)
    if ch_num == 2:
        continue

    module_name = ch_info["module"]
    proc_path = Path(f"processing/{module_name}.py")
    if not proc_path.exists():
        continue

    code = proc_path.read_text(encoding="utf-8")
    modified = False

    for sid in ch_info["series"]:
        if sid not in mapping:
            continue

        m = mapping[sid]
        src_id = m["source"]
        col_name = m["column"]

        # Find the source file for this source table
        src_entry = reg.get(src_id, {})
        src_file = src_entry.get("source_file", "")
        if not src_file:
            continue

        parts = src_file.split("/")
        ch_dir = parts[0] if len(parts) > 1 else f"ch{ch_num:02d}"
        fname = parts[-1]

        # Replace the generic "df.iloc[:, 0]" with the specific column
        func_pattern = f"def process_{sid.lower()}"
        if func_pattern in code:
            # Replace the primary column extraction
            old_pattern = f'        primary = df.iloc[:, 0].dropna()\n        primary = primary[primary.index.notna()]\n        if len(primary) == 0 and df.shape[1] > 1:\n            primary = df.iloc[:, 1].dropna()\n            primary = primary[primary.index.notna()]'
            new_pattern = f'        if "{col_name}" in df.columns:\n            primary = pd.to_numeric(df["{col_name}"], errors="coerce").dropna()\n        else:\n            primary = df.iloc[:, 0].dropna()\n        primary = primary[primary.index.notna()]'

            # Also handle derived series pattern
            old_derived = f'        primary = extracted.get("{sid}", extracted.get(list(extracted.keys())[0]) if extracted else pd.Series(dtype=float))'
            new_derived = f'        if "{col_name}" in df.columns:\n            primary = pd.to_numeric(df["{col_name}"], errors="coerce").dropna()\n        else:\n            primary = extracted.get("{sid}", extracted.get(list(extracted.keys())[0]) if extracted else pd.Series(dtype=float))'

            if old_pattern in code:
                code = code.replace(old_pattern, new_pattern, 1)
                modified = True
            elif old_derived in code:
                code = code.replace(old_derived, new_derived, 1)
                modified = True

    if modified:
        proc_path.write_text(code, encoding="utf-8")
        print(f"  Updated: {proc_path}")

print("Done")
