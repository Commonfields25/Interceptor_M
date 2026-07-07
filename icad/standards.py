"""
ICAD Engineering Standards
Standard dimensions for fasteners and manufacturing tolerances based on ISO and industrial catalogs.
"""


class Fasteners:
    # Socket Head Cap Screw (SHCS) Dimensions (ISO 4762)
    # Format: { 'clearance': dia, 'tap_drill': dia, 'head_dia': dia, 'head_height': dia }
    METRIC = {
        "M2": {
            "clearance": 2.4,
            "tap_drill": 1.6,
            "head_dia": 3.8,
            "head_height": 2.0,
            "counterbore_dia": 4.4,  # head_dia + 0.6 margin
            "counterbore_depth": 2.2,  # head_height + 0.2 margin
        },
        "M2.5": {
            "clearance": 2.9,
            "tap_drill": 2.05,
            "head_dia": 4.5,
            "head_height": 2.5,
            "counterbore_dia": 5.1,
            "counterbore_depth": 2.7,
        },
        "M3": {
            "clearance": 3.4,
            "tap_drill": 2.5,
            "head_dia": 5.5,
            "head_height": 3.0,
            "counterbore_dia": 6.5,  # head_dia + 1.0 margin for tool access
            "counterbore_depth": 3.3,  # head_height + 0.3 margin
        },
        "M4": {
            "clearance": 4.5,
            "tap_drill": 3.3,
            "head_dia": 7.0,
            "head_height": 4.0,
            "counterbore_dia": 8.0,
            "counterbore_depth": 4.4,
        },
        "M5": {
            "clearance": 5.5,
            "tap_drill": 4.2,
            "head_dia": 8.5,
            "head_height": 5.0,
            "counterbore_dia": 9.5,
            "counterbore_depth": 5.5,
        },
    }


class Tolerances:
    # Based on ISO 2768-m (Medium)
    LINEAR_MED = 0.1
    # Fit for shafts/holes
    H7_35mm = (0.0, 0.025)  # +0.025 / -0.0
    h7_35mm = (0.0, -0.025)  # +0.0 / -0.025


class Materials:
    AL_7075_DENSITY = 0.00281  # g/mm^3
    ASA_DENSITY = 0.00107  # g/mm^3


class Bearings:
    # Common miniature bearing dimensions (68x series)
    # { 'OD': mm, 'ID': mm, 'width': mm }
    SERIES_68 = {
        "6800": {"OD": 19.0, "ID": 10.0, "W": 5.0},
        "685": {"OD": 11.0, "ID": 5.0, "W": 5.0},
        "683": {"OD": 7.0, "ID": 3.0, "W": 3.0},
    }
    # Press-fit tolerance for housing (H7)
    HOUSING_TOLERANCE = Tolerances.H7_35mm
