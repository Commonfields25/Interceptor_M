---
agent: Jules
action: Mechanical Study
timestamp: 2026-07-05T15:19:01Z
status: Draft
---

# Mechanical Study: Folding Mechanisms & High-Speed Airframes

## 1. Folding Wings (DD-400 Line)

### 1.1 Constraints
- **Fuselage Diameter:** 35.0 mm
- **Launcher Bore:** 40.0 mm
- **Radial Clearance:** 2.5 mm per side
- **Target Wingspan:** 150 mm (deployed)

### 1.2 Proposed Mechanism: "Scissor-Back" Spring Deployment
Given the 2.5mm clearance, standard wrap-around wings (curved) are difficult to manufacture with AlSi10Mg.

**Design Strategy:**
- **Recessed Fuselage:** The fuselage (BRK-001) will feature four longitudinal slots (2.2mm deep) to house the wings during the launch phase.
- **Pivot Point:** Rear-mounted pivot with a torsion spring.
- **Locking:** Once the drone leaves the tube, springs deploy the wings to 90° (or 45° sweep). A centrifugal or spring-loaded pin locks them in the "flight" position.

### 1.3 Alternative: Flexible "Switchblade"
- High-tensile carbon fiber or spring steel plates that "pop" out.
- Advantages: Zero mechanical complexity.
- Disadvantages: Poor aerodynamic profile (flat plate).

---

## 2. F1-Chaser Concept (Rocket-Shaped Quad)

### 2.1 Architecture
The F1-Chaser is designed for maximum longitudinal speed to track fast targets.
- **Body:** Slender "Rocket" fuselage (40mm diameter for battery/avionics volume).
- **Propulsion:** 4x Brushless motors in "X" configuration.
- **Propellers:** 5-inch High-pitch (Pusher configuration preferred to keep clean air over the body).
- **Control:** Differential thrust for yaw/pitch/roll (no moving fins needed, reducing mass).

### 2.2 Aerodynamic Profile
- **Nose:** Tangent ogive for minimum drag.
- **Tail:** Tapered rear to reduce base drag.
- **Arms:** Integrated into the structural shell (monocoque) to minimize frontal area.

---

## 3. 2D Layout Plan (DXF Deliverables)

The following plans will be generated:
1. **DD-400_Assembly_2D**: Longitudinal section showing the nested wings and internal component stack (Seeker -> FC -> Battery -> Motor).
2. **F1-Chaser_Assembly_2D**: Top and side views of the rocket-quad, highlighting the "slender-body" design.
