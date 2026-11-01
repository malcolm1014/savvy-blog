# Teardown builds — proof of concept

Three self-contained, offline HTML pages built as a proof of concept for the
open-source **`teardown`** skill by **elvarofficial**
(<https://github.com/elvarofficial/teardown>), using Claude. Each one runs in a
browser with no install and no account — open the file and drag to orbit.

| File | What it is |
|------|------------|
| `atomic-clock.html` | A caesium-133 beam atomic clock you can fly into component by component — oven, state-selector magnets, Ramsey cavity, detector and electronics — with matter-wave atoms, an exploded view, a guided tour, and a live Eastern-time readout. |
| `cuckoo-clock.html` | A mechanical cuckoo clock: a weight-driven going train on a pendulum, plus a strike train that works the bellows and the bird on the hour. |
| `four-stroke-engine.html` | A single-cylinder four-stroke engine with a live pressure–volume indicator loop, driven by exact slider-crank geometry. |

## Honest scope
These are faithful **simulations and visualisations** of how each machine works —
not CAD models and not real instruments. The atomic clock models the real
quantities (the hyperfine states, ΔνCs = 9,192,631,770 Hz, Ramsey interrogation,
the servo lock); the time it shows comes from the viewer's own
network-synchronised clock, formatted to `America/New_York`.

## Credit
- **elvarofficial** — the `teardown` skill. MIT licensed.
- **whaleyxbt / claude-motion** (MIT) — the runtime `teardown` is built on.
- **Barty-Bart / motion-graphics** — CC0 Freesound samples.
- **mrdoob et al. / three.js** (MIT) — the 3D library every page uses.

Built by Malcolm R. Smith · Savvy Security LLC. Free to open, read and reuse.
