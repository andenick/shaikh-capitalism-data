# RSCD replicator `lib/` layout — anu-replicator v3.1 shared-helpers mapping

**Restructure:** A3 (post-v1.6). **Behavior-preserving** — an import-path refactor only;
no construction/validation logic changed. Verified by the 8-series offline smoke
(byte-identical before/after), `replicate.py --health` HEALTHY, and `run.py --gate` PASS.

## Why this layout

The anu-replicator **v3.1** spec (finding F-5C-01) prescribes a shared-helpers shape so
cross-series patterns (cached-API readers, panel/transform helpers, benchmark/anchor
validators, output writers) live in **one canonical place** instead of being scattered as
`_`-prefixed helpers inside the per-series phase dirs. RSCD ships 118 per-series loaders
(`L01_<sid>.py`), 118 processors (`P02_<sid>.py`) and 118 validators (`V03_<sid>.py`); the
shared helpers those files call are now consolidated under the four canonical dirs.

## The four canonical dirs (v3.1)

| v3.1 dir | Holds | RSCD canonical modules |
|----------|-------|------------------------|
| `lib/data/` | API/cache readers + source resolvers | `S00_apis.py`, `S00_cache.py`, `S00_config.py`, `_nipa_line_resolver.py`, `_nipa_t711_line_resolver.py`, `_bea_industry_loader.py`, `_ch6_appendix_loader.py`, `_imf_ifs_resolver.py` |
| `lib/transforms/` | Cross-series transform / panel-construction helpers | `_ayres_helper.py`, `_ch2_helpers.py`, `_ch3_helpers.py`, `_ch5_helpers.py`, `_ch9_helpers.py`, `_ch14_helpers.py`, `_ch16_helpers.py`, `_ch7_xlsx_panels.py`, `_inman_cost_curves.py`, `_ayres_processor.py`, `_ch7_industry_panel_processor.py` |
| `lib/validation/` | Anchor suite / benchmark + chapter validator libs | `_v03_anchor_lib.py`, `_ayres_validator.py`, `_ch14_validator_lib.py`, `_ch3_helpers.py`, `_ch7_validator_lib.py`, `_ch8_validator_lib.py` |
| `lib/io/` | Output writers (see deviation below) | pointer to `lib/O06_output/O06_chopped_writer.py`, `O06_extenbook_writer.py` |

## How imports keep working (zero per-series edits)

The orchestrator (`run.py`) puts `lib/` on `sys.path` and loads each phase script with
`importlib.util.spec_from_file_location`. Every per-series file imports helpers by their
**historical absolute package path**, e.g. `from L01_loaders._ch2_helpers import ...`,
`from S00_setup import S00_apis`, `from V03_validators._v03_anchor_lib import ...`.

Rather than rewrite ~350 files, each relocated helper leaves a **byte-stable back-shim** at
its old path. The shim is a `sys.modules` identity-alias:

```python
import importlib as _il, sys as _sys
_m = _il.import_module("transforms._ch2_helpers")
_sys.modules[__name__] = _m
```

This makes the old dotted name **the same module object** as the canonical one — every
symbol (including private `_names`), a single module identity, and shared module-level
mutable state all resolve unchanged. (`loaders/_imf_ifs_resolver.py` keeps its pre-existing
explicit re-export shim from the F-5A-03 hygiene pass; it now points through
`utils/_imf_ifs_resolver.py` → `data/_imf_ifs_resolver.py`.)

## Deviations from a literal v3.1 layout (deliberate, documented)

1. **Per-series `L01_<sid>.py` / `P02_<sid>.py` / `V03_<sid>.py` stay in their phase dirs.**
   The orchestrator discovers and dispatches per-series scripts from
   `L01_loaders/`, `P02_processors/`, `V03_validators/` (the `PHASE_DIRS`). Only the
   *shared* helpers were consolidated; the per-series triad is left in place by design.

2. **Writers stay in `lib/O06_output/`; `lib/io/` is a conformance pointer.**
   `O06_chopped_writer.py` and `O06_extenbook_writer.py` define a top-level `run()` and are
   **dispatched as phase scripts** from `O06_output/`. Relocating them would drop them from
   phase discovery and silently stop output generation. Additionally, a package literally
   named `io` shadows the Python standard-library `io` module, so `lib/io/` cannot serve
   live import submodules. `lib/io/` therefore documents where the writers live rather than
   holding them.

3. **`utils/paths.py` and `utils/vintage_manifest.py` stay in `lib/utils/`.**
   These are project path/vintage infrastructure (imported ~366× as `utils.paths`), not a
   data/transform/validation/io helper category. `lib/utils/` also retains the one-shot
   registry-mutator build scripts (`_phase*`, `_ch*_register`, `_docs_writer`), which are
   pipeline-authoring tools, not per-series shared runtime helpers.

## SKILL conformance note

Against anu-replicator SKILL.md (v3.1 `lib/{data,transforms,validation,io}`):
the four canonical dirs now **exist** and hold the consolidated cross-series shared helpers,
satisfying F-5C-01's intent (a shared-helper shape rather than a flat per-series lib). The
three deviations above are structural necessities of RSCD's orchestrator-dispatch model and
the `io`/stdlib name clash; each is behavior-preserving and covered by the gates. This is the
**deepest safe** realization: real code relocated into the canonical dirs (not merely
re-exported), with identity-alias back-shims preserving every existing import.
