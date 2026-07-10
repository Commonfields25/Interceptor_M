"""
PROP-022 — Front Lift Nacelle Motor Mount (G2)
Material: Al 7075-T6 | Process: CNC
"""
from build123d import *

def build_prop022(params: dict = None):
    params = params or {}
    bolt_circle = params.get("bolt_circle", 44.0)
    thickness = params.get("thickness", 6.0)

    with BuildPart() as p:
        with BuildSketch() as sk:
            Circle(bolt_circle/2 + 8)
            with Locations(PolarLocations(bolt_circle/2, 4).locations):
                Circle(4.2/2, mode=Mode.SUBTRACT) # M4 clearance
            Circle(10.0/2, mode=Mode.SUBTRACT) # Shaft bore
        extrude(amount=thickness)
    return p.part
