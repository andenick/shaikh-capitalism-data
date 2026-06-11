# RSCD — Reproduction Test

**Project**: Capitalism: Competition, Conflict, Crises (Shaikh 2016) Replication
**Framework**: Anu Framework v12.0 · Schema v2.3.0
**Latest verification**: 2026-05-27 (Phase PE, Opus testing subagent)
**Prior record**: 2026-05-22 (V5.1/V5.2 fresh-environment test — retained below)

---

## 1. Environment

| Item | Value |
|---|---|
| Platform | Windows 11 (win32) |
| Python | 3.13.7 (system; CI pins 3.11) |
| Replicator | `Technical/replicator/` — self-contained (`lib/` + `inputs_bundled/`), entry `scripts/replicate.py` |
| Bootstrap | replicator stands up a `workdir/RSCD/Technical/` tree from bundled inputs, sets `RSCD_PROJECT_ROOT`, imports the canonical `run.py` |
| API keys at test time | none in replicator (`--health` reports FRED/BEA/BLS MISSING → offline degradation path) |

---

## 2. Health + plan (replicator entry)

Run from `Technical/replicator/`:

| Check | Command | Result |
|---|---|---|
| Health | `python scripts/replicate.py --health` | **HEALTHY** — all required paths OK; core deps importable; registry parses 118 series; phase discovery S00=3, L01=118, P02=116, V03=118, O06=2. FRED/BEA/BLS keys reported MISSING (expected offline). |
| Plan | `python scripts/replicate.py --list` | OK — all phase scripts enumerated (exit 0). |

Note: the `--health` network/FRED probe did **not** fire on the replicator path because no key is configured — it cleanly reports MISSING and proceeds. (On the Publish-root `code/run.py --health`, with a `FRED_API_KEY` present in the environment, the live FRED probe ran and returned `{ok: True, rows: 1}`.)

---

## 3. Per-series offline reproduction (representative set)

Each series run via `python scripts/replicate.py --series <SID>`. Pipeline executed S00 (skipped — no keys) → L01 → P02 → V03 → O06. Regenerated `data/final/chopped/<SID>.csv` compared against the committed `Technical/chopped/<SID>.csv`.

### Recovered series (2026-05-26 figure-digitization recoveries)

| SID | V03 | Regenerated vs committed chopped | Source of recovery |
|---|---|---|---|
| S707 | PASS | **BYTE-IDENTICAL** | MPRA 51334 |
| S708 | PASS | **BYTE-IDENTICAL** | MPRA 51334 |
| S801 | PASS | **BYTE-IDENTICAL** | book PDF native-vector trace |
| S404 | PASS | **BYTE-IDENTICAL** | book PDF native-vector trace |
| S405 | PASS | **BYTE-IDENTICAL** | book PDF native-vector trace |
| S406 | PASS | **BYTE-IDENTICAL** | book PDF native-vector trace |
| S407 | PASS | **BYTE-IDENTICAL** | book PDF native-vector trace |

### Panel / theoretical series

| SID | V03 | Regenerated vs committed chopped |
|---|---|---|
| S705 | PASS | **BYTE-IDENTICAL** |
| S308 | PASS_THEORETICAL | **BYTE-IDENTICAL** |
| S218 | PASS | **BYTE-IDENTICAL** |

**Stability verdict**: 10/10 series reproduced. All ten regenerated chopped CSVs are **byte-for-byte identical** to the committed copies under `Technical/chopped/` (verified with `cmp -s`; not merely numerically close). S308 validates as `PASS_THEORETICAL`, the expected outcome for a theoretical/illustrative series — its CSV is still byte-identical. No failures, no fabrication.

Per-series wall-clock ~2–3 s on a warm cache. The ~160 s S00 network probe noted in the brief did not occur on the offline replicator path (no key → probe skipped).

---

## 4. Offline vs. API-key-dependent (honest scope)

| Category | Reproduces offline? | Notes |
|---|---|---|
| BOOK-PERIOD / offline series (incl. recovered S707, S708, S801, S404–S407) | **Yes** | Data bundled in `inputs_bundled/SalvagedInputs/`; L01 reads local files, no network. Verified byte-stable above. |
| Theoretical series (e.g. S308) | **Yes** | Deterministic construction (S1301 uses documented `SEED=42`); no network. |
| Panel series consumed by the offline set (e.g. S705) | **Yes** | Reproduced byte-identical. |
| EXTENSION (`-EXT`) subseries needing FRED/BEA/BLS | **No (degrades)** | Without `config/api_keys.env`, `--health` flags the keys MISSING and these series take the degradation path (book-period portion still builds; modern extension truncates/empties). Full extension reproduction requires `FRED_API_KEY` (and BEA/BLS for the BEA-/BLS-sourced extensions). |
| S703, S704 | **N/A** | `status: data_unavailable` by design (Christodoulopoulos Fig 7.13/7.14 spaghetti; recovery is guided WebPlotDigitizer, not a proxy). Not part of this test. |

Bottom line: the entire book-period / offline backbone — including all 7 recovered series — reproduces deterministically offline and byte-stably. Only the modern `-EXT` tails need live API keys, and their absence is reported by `--health` (no silent failure).

---

## 5. CI assessment

Two workflows exist under `.github/workflows/`:

### `ci.yml` — "RSCD CI" (on push / pull_request)
- `actions/checkout` → `setup-python@v5` (3.11)
- clean venv: `python -m venv .venv` → `pip install -r requirements.txt` ✔ (root `requirements.txt` present)
- `python code/run.py --health` and `python code/run.py --list` ✔ (both verified to run clean, exit 0, from the Publish root)
- `python check_project.py --project . || true`

**GAP (confirmed)**: `check_project.py` does **not exist** anywhere in the published tree (`find` returns nothing). The anu-doctor project-consistency step therefore cannot run. Because the step is suffixed with `|| true`, the job still reports green — so this is a *silent no-op*, not a build failure. Either (a) ship `check_project.py` (anu-doctor project mode) into the repo, or (b) drop the step. As written, the workflow's claim of "anu-doctor project consistency" is not actually exercised.

Minor: `ci.yml` does **not** run the replicator end-to-end or assert chopped reproduction. It checks health + plan only. A reproduction-diff step (run a small offline set, `cmp` against committed `chopped/`) would convert this test's manual byte-stability check into an enforced gate. (Not required by the brief; noted as an enhancement.)

### `replicator_check.yml` — "Replicator Check" (push/PR/weekly cron/dispatch)
- 3.11, pip cache, installs `Technical/replicator/requirements.txt`
- runs Phase 3 / Phase 4 validators if present (guarded by `-f`)
- writes `config/api_keys.env` from `secrets.FRED_API_KEY`/`BEA_API_KEY`, then `python scripts/replicate.py --report`
- uploads validation-report artifacts (`if: always()`)

This workflow is path-correct (targets `Technical/replicator/scripts/replicate.py`, which exists). It does **not** do a clean-venv `--health`/`--list` or `check_project`; it is the `--report`/validator-sweep complement to `ci.yml`. Note its paths (`Technical/**`, `replicator/**`) assume the full project tree, whereas `ci.yml` assumes a flattened publish layout (`code/`, root `requirements.txt`) — the two target slightly different repo shapes.

**CI status**: `ci.yml` install + health + list steps are sound and verified to pass; the `check_project.py` step is a confirmed gap (missing file, masked by `|| true`). `replicator_check.yml` is structurally correct for the replicator. Neither enforces chopped-output byte reproduction.

---

## Appendix — prior record (2026-05-22, V5.1/V5.2)

Fresh Python 3.11 venv → `pip install -r requirements.txt` → replicator orchestrator. Verified on source workspace:

| Check | Command | Result |
|---|---|---|
| Replicator health | `python code/run.py --health` | HEALTHY — registry 118 series |
| Plan enumeration | `python code/run.py --list` | all phase scripts discovered |
| Project consistency | `check_project.py --project .` | 0 failures / 0 warnings (run from source workspace, where the file exists) |
| Value validation | `VALIDATION_REPORT.json` | 118/118 series PASS at 1% tolerance |

(The 2026-05-22 "project consistency" check passed because it was run from the source workspace, which has `check_project.py`. The CI gap in §5 is that the *published* tree does not ship that file, so the CI step cannot reproduce that result.)
