"""
ICAD Parts — Build123d mechanical part definitions (L3 Manufacturing Grade)
All parts are parametric and export to STEP + STL via the CADEngine.
"""
from ocp_vscode import show

__all__ = [
    "build_brk001",
    "build_act001",
    "build_ncr001",
    "build_sabot001",
    "build_chs001",
    "build_wing001",
    "build_avs001",
    "build_bat3s001",
    "build_mmt001",
    "build_f1body01",
    "build_f1motor",
    "build_f1prop",
    "build_f1avs",
    "build_f1bat",
    "build_lnch001",
    "build_lnch002",
    "build_lnch003",
    "build_lnch004",
    "build_lnch005",
    "build_lnch006",
]

# ── Lazy import so `icad.engine` works without build123d at import time ──────
def __getattr__(name):
    mapping = {
        "build_brk001": "brk001",
        "build_act001": "act001",
        "build_ncr001": "ncr001",
        "build_sabot001": "sabot001",
        "build_chs001": "chs001",
        "build_wing001": "wing001",
        "build_avs001": "avs001",
        "build_bat3s001": "bat3s001",
        "build_mmt001": "mmt001",
        "build_f1body01": "f1body01",
        "build_f1motor": "f1motor",
        "build_f1prop": "f1prop",
        "build_f1avs": "f1avs",
        "build_f1bat": "f1bat",
        "build_lnch001": "lnch001",
        "build_lnch002": "lnch002",
        "build_lnch003": "lnch003",
        "build_lnch004": "lnch004",
        "build_lnch005": "lnch005",
        "build_lnch006": "lnch006",
    }
    mod_name = mapping.get(name)
    if mod_name:
        import importlib, sys
        mod = importlib.import_module(f"icad.parts.{mod_name}")
        obj = getattr(mod, name, None)
        if obj:
            sys.modules[__name__].__dict__[name] = obj
            return obj
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")