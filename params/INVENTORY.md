---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# params/ — Inventory

| File | Description |
|------|-------------|
| `params_DC.json` | Baseline parameters for the DD interceptor variant (mass, geometry, propulsion) |
| `params_DD.json` | Parameters for the DI interceptor (design target variant) |
| `params_DI.json` | Parameters for the DC interceptor variant |
| `hardware/prototypes/params*.json` | Prototype-level param overrides (see `hardware/prototypes/`) |

_Note:_ `hardware/prototypes/params*.json` contain variant-specific overrides used by `scripts/gen_geometry.py` for CAD generation.
