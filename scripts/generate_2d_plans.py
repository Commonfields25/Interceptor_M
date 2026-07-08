import ezdxf
import math
import os


def add_rect(msp, x, y, w, h, dxfattribs=None):
    msp.add_lwpolyline(
        [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], dxfattribs=dxfattribs
    )


def create_dd400_assembly(filename):
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    L, D = 380.0, 35.0
    R = D / 2.0
    L_nose = 122.5
    msp.add_line((0, 0), (L_nose, R))
    msp.add_line((0, 0), (L_nose, -R))
    msp.add_line((L_nose, R), (L, R))
    msp.add_line((L_nose, -R), (L, -R))
    msp.add_line((L, R), (L, -R))
    compartments = [80, 160, 240, 280]
    labels = ["SEEKER", "AVIONICS", "BATTERY", "ACTUATORS", "MOTOR"]
    prev_x = 0
    for i, x in enumerate(compartments):
        msp.add_line((x, R), (x, -R), dxfattribs={"linetype": "DASHED"})
        msp.add_text(labels[i], dxfattribs={"height": 5}).set_placement(
            ((prev_x + x) / 2, -5)
        )
        prev_x = x
    msp.add_text(labels[-1], dxfattribs={"height": 5}).set_placement(
        ((prev_x + L) / 2, -5)
    )
    add_rect(msp, 140, R - 2, 60, 2, dxfattribs={"color": 1})
    add_rect(msp, 140, -R, 60, 2, dxfattribs={"color": 1})
    msp.add_line((0, 20), (L, 20), dxfattribs={"color": 2, "linetype": "CENTER"})
    msp.add_line((0, -20), (L, -20), dxfattribs={"color": 2, "linetype": "CENTER"})
    doc.saveas(filename)


def create_dd400_wing_mechanism(filename):
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    msp.add_circle((0, 0), 2.5)
    msp.add_text("PIVOT M2.5", dxfattribs={"height": 2}).set_placement((3, 3))
    add_rect(msp, -60, -2, 60, 4, dxfattribs={"color": 1})
    msp.add_lwpolyline(
        [(0, 0), (75, 0), (75, 4), (0, 4), (0, 0)],
        dxfattribs={"color": 8, "linetype": "DASHED"},
    )
    doc.saveas(filename)


def create_f1_chaser_assembly(filename):
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    L, D = 400.0, 40.0
    R = D / 2.0
    msp.add_line((0, 0), (100, R))
    msp.add_line((0, 0), (100, -R))
    msp.add_line((100, R), (350, R))
    msp.add_line((100, -R), (350, -R))
    msp.add_line((350, R), (L, R - 10))
    msp.add_line((350, -R), (L, -(R - 10)))
    msp.add_line((L, R - 10), (L, -(R - 10)))
    msp.add_circle((150, R + 10), 63.5, dxfattribs={"color": 3})
    msp.add_circle((150, -(R + 10)), 63.5, dxfattribs={"color": 3})
    msp.add_circle((300, R + 10), 63.5, dxfattribs={"color": 3})
    msp.add_circle((300, -(R + 10)), 63.5, dxfattribs={"color": 3})
    doc.saveas(filename)


def create_generic_assembly(filename, L, D, label):
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    R = D / 2.0
    L_nose = L * 0.32
    msp.add_line((0, 0), (L_nose, R))
    msp.add_line((0, 0), (L_nose, -R))
    msp.add_line((L_nose, R), (L, R))
    msp.add_line((L_nose, -R), (L, -R))
    msp.add_line((L, R), (L, -R))
    msp.add_text(f"{label} ASSEMBLY", dxfattribs={"height": 10}).set_placement(
        (L / 4, 50)
    )
    doc.saveas(filename)


if __name__ == "__main__":
    os.makedirs("models/DD", exist_ok=True)
    os.makedirs("models/DI", exist_ok=True)
    os.makedirs("models/DC", exist_ok=True)
    os.makedirs("models/F1", exist_ok=True)
    create_dd400_assembly("models/DD/DD-400_Assembly_2D.dxf")
    create_dd400_wing_mechanism("models/DD/DD-400_Wing_Mechanism_2D.dxf")
    create_f1_chaser_assembly("models/F1/F1-Chaser_Assembly_2D.dxf")
    create_generic_assembly("models/DI/DI-300_Assembly_2D.dxf", 365.0, 35.0, "DI-300")
    create_generic_assembly("models/DC/DC-250_Assembly_2D.dxf", 350.0, 35.0, "DC-250")
