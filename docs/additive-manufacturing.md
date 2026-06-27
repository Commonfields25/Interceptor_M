# Interceptor_M — Additive Manufacturing Analysis

## Executive Summary
Additive manufacturing (AM) is evaluated for three production scenarios:

| Part | Recommended AM Process | Rationale |
|---|---|---|
| BRK-001 | **DMLS (AlSi10Mg)** | Topology-optimised lattice, complex bore/hole geometry, batch ≥ 10 units |
| ACT-001 | **DMLS (AlSi10Mg)** | Thin pockets (8.5 mm depth), high density required, ESC/FC fit critical |
| NCR-001 | **DMLS (316L SS)** | Superior surface finish for bore sealing; O-ring groove as-built acceptable |

> **Note:** Prototype machining remains the preferred path for first articles (< 5 units) 
> due to predictability, existing tooling, and CMM traceability. AM is recommended 
> for **serial production ≥ 10 units** where geometry complexity or part count 
> justifies the tooling investment.

---

## 1. BRK-001 — Structural Junction Bracket

### AM Candidate Processes
| Process | Material | Build resolution | Surface finish | Cost |
|---|---|---|---|---|
| DMLS | AlSi10Mg | 20–30 µm | Ra 5–10 µm | €€€ |
| SLM | Al7075 | 30 µm | Ra 8–15 µm | €€€ |
| Binder Jetting | AlSi10Mg | 50 µm | Ra 10–15 µm | €€ |
| FDM | PLA/CF-Nylon | 100 µm | Ra 100–200 µm | € |

### Recommended: **DMLS — AlSi10Mg**
- As-built: 380 MPa UTS, 40% elongation — exceeds 7075-T6 structural requirements
- Lattice infill option for mass reduction (target: 15% mass saving vs machined)
- As-built surface: Ra 5–8 µm → light bead-blast → Ra ≤ 1.6 µm achievable
- Post-process: stress-relief 300 °C 2 h + T6 heat treatment → 490 MPa UTS

### Build Layout
- Build direction: Z-axis (bore axis) — best for bore surface quality
- Support strategy: tree-style from bottom face; minimal on bore wall
- Batch: 9 parts (3 lines × 3 units) per build plate

### Design Notes for AM
- Minimum wall thickness: 1.5 mm (DMLS AlSi10Mg spec)
- Minimum feature size (as-built): Ø1.0 mm holes (≥ 2.5 mm for functional bores)
- Add fillet radii R ≥ 0.5 mm at all internal corners (stress concentration)

---

## 2. ACT-001 — Actuator Mount

### AM Candidate Processes
| Process | Material | Build resolution | Surface finish | Cost |
|---|---|---|---|---|
| DMLS | AlSi10Mg | 20–30 µm | Ra 5–10 µm | €€€ |
| SLM | Al7075 | 30 µm | Ra 8–15 µm | €€€ |
| FDM | CF-Nylon | 100 µm | Ra 100 µm | € |

### Recommended: **DMLS — AlSi10Mg**
- ESC and FC pockets require Ra ≤ 1.6 µm for flat seating — achievable with light milling of pocket floors post-build (0.3 mm finish cut)
- M2/M3 clearance holes: DMLS as-built Ø2.2/Ø3.3 mm functional without tapping (use helicoil inserts if threads needed)
- Lattice infill reduces mass from 55.49 g → 45 g (estimated 18% saving)

### Post-AM Process
1. Stress-relief 300 °C 2 h
2. Support removal + bead-blast
3. Light CNC finish on pocket floors (Op 30 equivalent, 0.3 mm DOC)
4. Alodine 1200S + MIL-PRF-23377 primer

---

## 3. NCR-001 — Nose-Cone Interface Ring

### AM Candidate Processes
| Process | Material | Build resolution | Surface finish | Cost |
|---|---|---|---|---|
| DMLS | 316L SS | 20–30 µm | Ra 5–8 µm | €€€ |
| EBM | Ti6Al4V | 50 µm | Ra 20–30 µm | €€€ |
| SLM | 316L SS | 30 µm | Ra 8–12 µm | €€€ |
| FDM + layup | Nomex/CF | 200 µm | Ra 200 µm | € |

### Recommended: **DMLS — 316L SS**
- Bore sealing surface (Ø35 mm) and O-ring groove (Ø36.5 mm) require Ra ≤ 1.6 µm
- DMLS as-built: Ra 5–8 µm — requires light post-machining (2–3 passes) for groove
- NDT required: X-ray CT for internal porosity (aerospace grade)

### Alternative for NCR-001: **Hybrid DMLS + Machining**
1. DMLS build (bore and OD near-net-shape)
2. Post-AM turning on bore/OD (Op 30/40 equivalent)
3. O-ring groove milled on 5-axis or turned on lathe

> Hybrid approach is preferred for volumes 5–50 units where DMLS geometry 
> complexity is exploited but surface finish is guaranteed.

---

## 4. Additive Manufacturing Envelope

### Interceptor_M Build Envelope Requirements
| Parameter | Value |
|---|---|
| Max part dimension | 100 mm (BRK-001 length axis) |
| Min feature | Ø2.0 mm (functional hole) |
| Wall thickness min | 1.5 mm (DMLS AlSi10Mg) |
| Tolerance as-built | ±0.3% (ISO/ASTM) |
| Tolerances post-machined | ±0.05 mm |

### Machine Candidates
| Machine | Material | Build vol. | Notes |
|---|---|---|---|
| EOS M 290 | AlSi10Mg / 316L | 250×250×325 mm | Industry standard; SP limited |
| SLM 280 2.0 | AlSi10Mg / 316L | 280×280×365 mm | Twin-laser option |
| Trumpf TruPrint 3000 | AlSi10Mg | 300×300×300 mm | Integrated induction seal |

---

## 5. Design for AM — Summary Rules

1. **Orientation**: bore axis vertical (Z) for BRK/NCR; flat-face parts with pockets upward
2. **Supports**: tree-structure from flat bottom faces; avoid supports on sealing surfaces
3. **Lattice infill**: BCCZ (body-centred cubic Z) at 20% density for structural brackets
4. **Minimum wall**: 1.5 mm AlSi10Mg, 2.0 mm 316L SS
5. **Surface**: Ra 5–8 µm as-built; add 0.3–0.5 mm stock for post-machining
6. **NDT**: X-ray CT scan all structural brackets; helium leak test NCR bore

---

## 6. AM Qualification Checklist

| Item | BRK-001 | ACT-001 | NCR-001 |
|---|---|---|---|
| Process spec | DMLS AlSi10Mg | DMLS AlSi10Mg | DMLS 316L SS |
| Post-AM machining | None (as-built) | Pocket floor finish | Bore/OD + groove |
| Surface treatment | Alodine + primer | Alodine + primer | Passivate + bead-blast |
| NDT required | CT scan + tensile coupon | CT scan | CT scan + leak test |
| Batch size for economics | ≥ 10 units | ≥ 10 units | ≥ 5 units |
| Unit cost estimate (10 units) | €45–60 | €35–50 | €50–70 |
