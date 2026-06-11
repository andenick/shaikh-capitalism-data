"""P0 bootstrap for the Perfect-Replication campaign:
(1) back up mutable artifacts, (2) build REPLICATION_GROUNDTRUTH_INDEX.json,
(3) seed RSCD_REPLICATION_STATE.json with the full P0-P8 task ledger.
Idempotent: re-running refreshes the index + backup but preserves existing task statuses.
"""
import json, shutil, datetime, glob
from pathlib import Path
from utils import paths

UTC = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
T = paths.TECHNICAL
reg = json.load(open(paths.REGISTRY, encoding='utf-8'))
series = reg['series']

# ---- P0.1 backup ----
bk = T / "tmp" / f"repl_backup_{UTC}"
(bk / "docs_series").mkdir(parents=True, exist_ok=True)
for f in ["series_registry.json", "SUBSOURCE_METADATA.json", "ANU_LEDGER.json",
          "PIPELINE_STATE.json", "VALIDATION_REPORT.json"]:
    if (T / f).exists():
        shutil.copy2(T / f, bk / f)
for dpr in glob.glob(str(paths.DOCS_SERIES / "*_DPR.md")):
    shutil.copy2(dpr, bk / "docs_series" / Path(dpr).name)

# ---- P0.2 ground-truth index ----
linkage = {}
if paths.KB_LINKAGE.exists():
    try: linkage = json.load(open(paths.KB_LINKAGE, encoding='utf-8'))
    except Exception: linkage = {}
chopped_tables = sorted(p.name for p in (paths.SALVAGED_BOOK_DATA / "ShaikhChoppedTables").glob("*")
                        ) if (paths.SALVAGED_BOOK_DATA / "ShaikhChoppedTables").exists() else []
gt = {"generated_at": UTC, "n_series": len(series),
      "shaikh_chopped_tables": chopped_tables, "series": {}}
for sid, s in series.items():
    gt["series"][sid] = {
        "name": s.get("name"), "chapter": s.get("chapter"),
        "figures": s.get("figures", []), "content_type": s.get("content_type"),
        "status": s.get("status"), "construction": s.get("construction"),
        "proxy": bool(s.get("proxy")),
        "chopped_exists": (paths.CHOPPED_DIR / f"{sid}.csv").exists(),
        "dpr": s.get("dpr"),
    }
json.dump(gt, open(T / "REPLICATION_GROUNDTRUTH_INDEX.json", "w", encoding='utf-8'), indent=2)

# ---- P0.3 seed state ledger ----
chapters = sorted({s.get("chapter") for s in series.values() if isinstance(s.get("chapter"), int)})
da = [sid for sid, s in series.items() if s.get("status") == "data_unavailable"]
proxies = [sid for sid, s in series.items() if s.get("proxy")]

def T_(status="pending", **kw): return {"status": status, "attempts": 0, "validator": None, "notes": "", **kw}

tasks = {}
tasks["P0.1_backup"] = T_("done", outputs=[str(bk)])
tasks["P0.2_groundtruth"] = T_("done", outputs=["Technical/REPLICATION_GROUNDTRUTH_INDEX.json"])
tasks["P0.3_seed"] = T_("done")
# P1 coverage (value-per-effort order)
for sid in ["S801", "S404", "S405", "S406", "S407", "S703", "S704"]:
    tasks[f"P1.{sid}"] = T_(inputs=[gt["series"].get(sid, {}).get("figures")],
                            acceptance="status flipped off data_unavailable + V03 PASS + chopped + extenbook, OR exhaustive ladder documented")
# P2 value-check + P3 figure-repro per chapter
for ch in chapters:
    tasks[f"P2.ch{ch:02d}"] = T_(acceptance="book-period values reconcile to the book (non-circular); divergences fixed/explained")
    tasks[f"P3.ch{ch:02d}"] = T_(acceptance="every chapter figure/table reproduced & matched, or mismatch explained")
tasks["P2.ES"] = T_(); tasks["P2.AS"] = T_()
# P4 method fidelity
tasks["P4.proxy"] = T_(inputs=proxies, acceptance="each proxy has valid concept-match justification")
tasks["P4.formula"] = T_(acceptance="formula/composite series recompute Shaikh's method from public components; no lazy splices")
# P5
tasks["P5.1_ceiling"] = T_(); tasks["P5.2_triage"] = T_()
# P6
tasks["P6.1_refvalues"] = T_(acceptance="118/118 book-anchored reference_values")
tasks["P6.2_replicator"] = T_()
# P7
tasks["P7.1_cleanvenv"] = T_(); tasks["P7.2_ci"] = T_()
# P8 (needs anu skills)
for t in ["P8.1_review", "P8.2_reports", "P8.3_release", "P8.4_handoff"]:
    tasks[t] = T_(notes="needs anu skill (anu-doctor/anu-build/anu-publish)")

state_path = T / "RSCD_REPLICATION_STATE.json"
if state_path.exists():
    old = json.load(open(state_path, encoding='utf-8'))
    for k, v in old.get("tasks", {}).items():        # preserve prior progress
        if k in tasks and v.get("status") in ("done", "in_progress", "blocked"):
            tasks[k] = v
state = {"schema": "rscd-replication-v1", "updated_at": UTC, "current_phase": "P1",
         "data_unavailable_remaining": da, "proxies": proxies, "chapters": chapters,
         "gates": {p: "open" for p in ["P0","P1","P2","P3","P4","P5","P6","P7","P8"]},
         "anu_doctor": {"last_run": None, "available_this_session": False},
         "backups": [str(bk)], "tasks": tasks}
state["gates"]["P0"] = "passed"
json.dump(state, open(state_path, "w", encoding='utf-8'), indent=2)

print("P0 done.")
print("  backup:", bk)
print("  groundtruth index:", T / "REPLICATION_GROUNDTRUTH_INDEX.json", "| chopped tables:", len(chopped_tables))
print("  state:", state_path)
print("  chapters:", chapters)
print("  P1 data_unavailable to recover:", da)
print("  proxies:", proxies)
print("  total tasks:", len(tasks), "| pending:", sum(1 for v in tasks.values() if v["status"] == "pending"))
