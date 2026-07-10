# Mass Audit & Remediation Strategy (INT-202)

## 1. Audit Summary
- **Current BOM Total**: 8587.00 g
- **Target MTOW**: 6000.00 g
- **Mass Overshoot**: 2587.00 g (+43.1%)

### Subsystem breakdown (pre-remediation):
- **Propulsion**: 3795.00 g (44.2%)
- **Fuselage**: 2281.00 g (26.6%)
- **Wing**: 1080.00 g (12.6%)
- **Structure/Tail/Avionics**: 1431.00 g (16.6%)

## 2. Remediation Strategy: Option C (Hybrid)
To achieve the 6000g MTOW target, a combination of propulsion scope reduction and aggressive structural lightening is required.

### 2.1 Propulsion Reduction (Total saving: ~1250g)
1. **Switch to 2+2 Configuration**: Remove dedicated front lift motors (PROP-001/002) and associated hardware. Tilt-rotors (PROP-009/010) will handle both vertical lift and horizontal cruise.
   - *Motor saving*: -360g
   - *ESC saving*: -140g
   - *Prop/Nacelle saving*: -320g
2. **Battery Optimization**: Replace 12S 5000mAh (780g) with high-density 12S 3300mAh.
   - *Battery saving*: -250g
3. **PDB Lightening**: Switch to integrated PCB-based distribution.
   - *PDB saving*: -180g

### 2.2 Structural Lightening (Total saving: ~1350g)
1. **Fuselage Optimization**: Use Ultra-High Modulus Carbon Fiber with 1.0mm wall thickness for non-load-bearing sections.
   - *FUS-001 saving*: -280g
   - *FUS-002/006/009 saving*: -220g
2. **Wing Re-engineering**: Switch from solid sandwich to rib-and-skin construction with 0.5mm CF skins.
   - *WNG-001/002 saving*: -450g
3. **Tail Boom & X-Tail**: Use thinner wall Ø20mm tubes and hollow-core tail surfaces.
   - *TAIL/XTAL saving*: -250g
4. **Fastener Audit**: Replace SS A2-70 bolts with Titanium/Nylon where appropriate.
   - *STR-* saving*: -150g

## 3. Post-Remediation Estimate
- **Total Saving**: 2600 g
- **Estimated New BOM Mass**: 5987 g
- **Margin to MTOW**: 13 g

## 4. Implementation
The BOM (`docs/v3/V3_BOM_complete.csv`) will be updated in the next step to reflect these specific mass targets.
