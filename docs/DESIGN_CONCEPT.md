# Interceptor M — Design Concept & Ergonomics
**Issue:** #71  
**Version:** 1.0  
**Classification:** Confidential

---

## 1. Moodboard

### Visual References
| Theme | Reference | Rationale |
|---|---|---|
| **Silhouette** | Stealth aircraft / loitering munition | Low observability aesthetic; reinforces ISR mission role |
| **Surface language** | Riveted titanium aerospace panels, flush fasteners | Industrial, rugged, mission-grade |
| **Colour psychology** | Matte black + safety orange accents | Stealth base + field visibility + urgency |
| **Typography** | Monospace / stencil | Military documentation feel |
| **Texture** | Shot-peened AlSi10Mg surface, bead-blasted brackets | Functional surface treatment for fatigue resistance |

### Form Language Keywords
`angular` · `flush` · `low-observable` · `modular` · `ruggedised`

### Visual Narrative
> *Interceptor M is the operational tool of a precision ISR payload. Its visual language should communicate controlled aggression — the calm confidence of a system that has been designed down to the last gram.*

---

## 2. Color Palette

### Primary System
| Name | Hex | Usage |
|---|---|---|
| **Matte Black** | `#1A1A1A` | Primary structural surfaces, airframe |
| **Titanium Grey** | `#4A4F5A` | Brackets, PCB shields, secondary structure |
| **Safety Orange** | `#FF6B00` | Kill-tag indicators, payload release actuators, emergency markers |
| **Lab White** | `#E8E8E8` | Labels, stencil markings, human-interface surfaces |
| **Signal Green** | `#00C851` | Status LEDs, healthy-state indicators |
| **Alert Red** | `#FF4444` | Fault indicators, fail-safe states |
| **Graphite** | `#2D2D2D` | Internal frame, PCB substrate colour reference |

### Finishes & Surface Treatment
- **DMLS parts:** As-built shot-peened AlSi10Mg, no post-coat (weight saving)
- **CNC machined parts:** Clear anodise (MIL-A-8625 Type II)
- **3D-printed sabot:** Matte ASA, natural grey `#8A8A8A`
- **Fasteners:** Passivated stainless, flat black

### Marquage / Labelling
- Stencil paint, **Lab White `#E8E8E8`**, on **Matte Black `#1A1A1A`** surfaces
- Part numbers per `BOM_BASELINE.md` nomenclature
- Serialisation QR code on primary structure

---

## 3. Ergonomics

### Take-Up / Handing
| Concern | Solution |
|---|---|
| **Weight** | `< 2.5 kg AUW` — single-hand carry with caged payload bay |
| **Centre of gravity** | 30% from nose — carry handle at 28% chord |
| **Grip surface** | Shot-peened texture on carry handle bar; no sharp edges (r>2mm) |
| **Dust/water** | IP54 minimum on electronic bays; silicone gasket on payload bay door |
| **Field replacement** | Tool-free payload bay door (quarter-turn fasteners); 5-min FC swap |

### Assembly Ergonomics
- **Top-load integration**: Battery and payload inserted from top, reducing flip frequency
- **Keyed connectors**: USB-C power, JST-GH安全, no媒ot mistmatch possible
- **Magnetic retention**: Payload bay door uses 4× N52 neodymium magnets
- **Service access**: Two-panel access (top + aft); all connectors within 50 mm of panel edge

### Maintenance Philosophy
> *Every field service action must be executable in ≤ 5 minutes by a single operator without tools, in ambient temperature, with gloves.*

---

## 4. Silhouette & Proportions

### Overall Dimensions
| Parameter | Value |
|---|---|
| **Length** | 480 mm (tube constraint Ø40mm integrated) |
| **Max diameter** | Ø40 mm main tube |
| **Wingspan** | 340 mm |
| **Height** | 85 mm (with landing gear deployed) |
| **Fin span** | 200 mm (biface) |

### Proportional Analysis
```
     ████  ← 40mm tube (aspect ratio driven)
    ██████
   █████████
  ████████████  ← SABOT interface section
  ┃         ┃  ← wing at 65% chord
  ████████████
     ████
     ████  ← tail fins
```

### Structural Language
- **Smooth tapering**: Nose section blends from Ø40 mm to Ø20 mm over 120 mm
- **No protrusions** below the tube envelope except landing gear (retractable)
- **Fins**: Twin biface, 12° sweep, NACA 0012 equivalent section
- **SABOT interface**: cylindrical CAD model `SABOT-001.stl` — circular shear-ring feature

### Design Language Summary
| Attribute | Expression |
|---|---|
| **Primary form** | Cylindrical tube + integrated sabot section |
| **Secondary form** | Flat-plate wings, flush-fastener skin |
| **Accent** | Safety orange kill-tag ring at 70% chord |
| **Surface** | Shot-peened / bead-blasted (functional + aesthetic) |
| **Scale reference** | Human hand (single-operator carry) |

---

*Produced for Issue #71 — G2 Readiness Program — Interceptor M v1.5*
