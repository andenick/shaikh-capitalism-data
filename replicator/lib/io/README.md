# lib/io/ — output writers (conformance pointer)

The anu-replicator v3.1 spec places output writers under `lib/io/`.
In RSCD the chopped/extenbook writers (`O06_chopped_writer.py`,
`O06_extenbook_writer.py`) define a top-level `run()` and are
**dispatched by the orchestrator** (`run.py`) from `lib/O06_output/`
as phase scripts. Relocating them would remove them from phase
discovery and silently stop output generation, so they remain in
`lib/O06_output/`.

Additionally, a package literally named `io` shadows the Python
standard-library `io` module, so `lib/io/` cannot serve live import
submodules. It is therefore a documented conformance marker. The
canonical writers live at `lib/O06_output/O06_*_writer.py`.

See `lib/LAYOUT.md`.
