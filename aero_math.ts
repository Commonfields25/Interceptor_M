/**
 * AeroMath — Aerodynamic & Structural Design Functions
 * Project: Interceptor_M VTOL Drone
 * Version: 1.0.0
 */

// ─── Core Units ────────────────────────────────────────────────────────────────
const MM = 1;
const CM = 10 * MM;
const M  = 1000 * MM;

// ─── Wing Geometry ─────────────────────────────────────────────────────────────
export interface WingGeometry {
  span_mm: number;
  rootChord_mm: number;
  tipChord_mm: number;
  sweep_deg: number;
  dihedral_deg: number;
}

/** Taper ratio λ = tipChord / rootChord */
export function taperRatio(wing: WingGeometry): number {
  return wing.tipChord_mm / wing.rootChord_mm;
}

/** Mean Aerodynamic Chord (MAC) — formula: 2/3·c_r·(1−λ+λ²)/(1+λ) */
export function meanAerodynamicChord(wing: WingGeometry): number {
  const lambda = taperRatio(wing);
  const cr = wing.rootChord_mm;
  return (2 / 3) * cr * (1 - lambda + lambda ** 2) / (1 + lambda);
}

/** Wing Area S = ½·span·(c_r + c_t) */
export function wingArea(wing: WingGeometry): number {
  return 0.5 * wing.span_mm * (wing.rootChord_mm + wing.tipChord_mm);
}

/** Aspect Ratio AR = b² / S */
export function aspectRatio(wing: WingGeometry): number {
  const S = wingArea(wing);
  return (wing.span_mm ** 2) / S;
}

/** Distance from root leading edge to MAC leading edge along span */
export function MAC_LE_position(wing: WingGeometry): number {
  const lambda = taperRatio(wing);
  // x_LE = (b/6)·(1 + 2λ)/(1 + λ)
  return (wing.span_mm / 6) * ((1 + 2 * lambda) / (1 + lambda));
}

/** Aerodynamic center as % of MAC from LE (approx 25% for subsonic) */
export function aerodynamicCenter_MAC(wing: WingGeometry): number {
  return 0.25 * meanAerodynamicChord(wing);
}

// ─── Airfoil Data ──────────────────────────────────────────────────────────────
export interface Airfoil {
  name: string;
  Cl_max: number;
  Cl_alpha_per_rad: number;
  Cd0: number;
  alpha Stall_deg: number;
}

/** Lift coefficient at given angle of attack (thin airfoil theory) */
export function liftCoefficient(af: Airfoil, alpha_deg: number): number {
  const alpha_rad = alpha_deg * (Math.PI / 180);
  return af.Cl_alpha_per_rad * (alpha_rad - af.alpha_stall_deg * Math.PI / 180);
}

/** Induced drag coefficient CD_i = CL² / (π·e·AR) */
export function inducedDragCoefficient(
  Cl: number,
  wing: WingGeometry,
  Oswald_efficiency: number = 0.8
): number {
  const AR = aspectRatio(wing);
  return (Cl ** 2) / (Math.PI * Oswald_efficiency * AR);
}

/** Total drag C_D = C_D0 + C_Di */
export function totalDragCoefficient(
  Cd0: number,
  Cl: number,
  wing: WingGeometry,
  e: number = 0.8
): number {
  return Cd0 + inducedDragCoefficient(Cl, wing, e);
}

/** Lift-to-drag ratio L/D = C_L / C_D */
export function liftToDrag(Cl: number, Cd: number): number {
  return Cl / Cd;
}

// ─── Structural ────────────────────────────────────────────────────────────────
export interface Material {
  name: string;
  density_g_cm3: number;
  E_GPa: number;
  sigma_yield_MPa: number;
}

/** Wing mass estimate (kg) — foam core + skins */
export function wingMassEstimate(
  wing: WingGeometry,
  foamDensity_g_cm3: number = 0.033,
  skinThickness_mm: number = 0.4,
  skinLayers: number = 2
): number {
  const S_cm2 = wingArea(wing) / 100;           // mm² → cm²
  const span_cm = wing.span_mm / 10;
  const chord_cm = wing.rootChord_mm / 10;

  const foamVol_cm3 = S_cm2 * chord_cm * 0.3;   // assume 30% chord thickness
  const foamMass_g  = foamVol_cm3 * foamDensity_g_cm3 * 1000;

  const skinArea_cm2 = 2 * skinLayers * S_cm2;
  const skinMass_g   = skinArea_cm2 * (skinThickness_mm / 10) * 1.6; // ~1.6 g/cm³ fiberglass

  return (foamMass_g + skinMass_g) / 1000;
}

// ─── Flight Performance ────────────────────────────────────────────────────────
export interface FlightCondition {
  velocity_m_s: number;
  airDensity_kg_m3: number;  // rho, default 1.225 at sea level
  altitude_m: number;
}

export const stdAtmosphere = {
  rho0: 1.225,
  scaleHeight_m: 8500,
};

export function airDensity(altitude_m: number): number {
  return stdAtmosphere.rho0 * Math.exp(-altitude_m / stdAtmosphere.scaleHeight_m);
}

/** Dynamic pressure q = ½·ρ·v² */
export function dynamicPressure(v_m_s: number, rho_kg_m3: number): number {
  return 0.5 * rho_kg_m3 * v ** 2;
}

/** Required lift coefficient CL = 2·W / (ρ·v²·S) */
export function requiredLiftCoefficient(
  weight_N: number,
  v_m_s: number,
  wing: WingGeometry,
  rho_kg_m3: number = 1.225
): number {
  const S_m2 = wingArea(wing) / 1_000_000;
  return (2 * weight_N) / (rho_kg_m3 * v ** 2 * S_m2);
}

/** Stall speed v_stall = sqrt(2·W / (ρ·S·Cl_max)) */
export function stallSpeed(
  weight_N: number,
  wing: WingGeometry,
  Cl_max: number,
  rho_kg_m3: number = 1.225
): number {
  const S_m2 = wingArea(wing) / 1_000_000;
  return Math.sqrt((2 * weight_N) / (rho_kg_m3 * S_m2 * Cl_max));
}

// ─── Wing Blueprint Drawing ────────────────────────────────────────────────────
export interface BlueprintOptions {
  scale: number;        // px per mm
  showMAC: boolean;
  showGrid: boolean;
  showDimensions: boolean;
  title: string;
}

export function drawWingSVG(
  wing: WingGeometry,
  opts: Partial<BlueprintOptions> = {}
): string {
  const {
    scale = 2,
    showMAC = true,
    showGrid = true,
    showDimensions = true,
    title = "Wing Blueprint",
  } = opts;

  const s  = scale;
  const b  = wing.span_mm;
  const cr = wing.rootChord_mm;
  const ct = wing.tipChord_mm;
  const sw = wing.sweep_deg;

  // Canvas size
  const pad   = 40;
  const W     = (cr + b * Math.tan(sw * Math.PI / 180) + ct) * s + pad * 2;
  const H     = b * s + pad * 2;

  // Origin (root LE)
  const ox = pad + cr * s;
  const oy = pad;

  // Points
  const RLE  = [ox, oy];
  const RTE  = [ox - cr * s, oy];
  const TLE  = [pad + b * Math.tan(sw * Math.PI / 180), pad + b * s];
  const TTE  = [TLE[0] - ct * s, TLE[1]];

  const cx = [RLE[0], RTE[0], TTE[0], TLE[0]];
  const cy = [RLE[1], RTE[1], TTE[1], TLE[1]];

  // MAC position
  const mac     = meanAerodynamicChord(wing);
  const macX    = MAC_LE_position(wing);
  const mac_cx  = ox - (cr - macX) * s;
  const mac_cy  = oy + macX * s * Math.tan(sw * Math.PI / 180);

  const lines: string[] = [];
  const texts: string[] = [];

  // Grid
  if (showGrid) {
    for (let x = pad; x < W; x += 50 * s) {
      lines.push(`<line x1="${x}" y1="${pad}" x2="${x}" y2="${H - pad}" stroke="#ddd" stroke-width="0.5"/>`);
    }
    for (let y = pad; y < H; y += 50 * s) {
      lines.push(`<line x1="${pad}" y1="${y}" x2="${W - pad}" y2="${y}" stroke="#ddd" stroke-width="0.5"/>`);
    }
  }

  // Wing outline
  lines.push(
    `<polygon points="${cx.join(',')}" fill="#e8f4ff" stroke="#2c3e50" stroke-width="2"/>`
  );

  // Rib lines (every 50mm)
  for (let y = 50 * s; y < b * s; y += 50 * s) {
    const frac = y / (b * s);
    const x0   = ox - cr * s + frac * (TLE[0] - (ox - cr * s));
    const chord_at = cr * (1 - frac * (1 - ct / cr));
    lines.push(`<line x1="${x0}" y1="${oy + y}" x2="${x0 + chord_at * s}" y2="${oy + y}" stroke="#aaa" stroke-width="0.5" stroke-dasharray="4,2"/>`);
  }

  // MAC
  if (showMAC) {
    const macW = mac * s;
    const macH = 6;
    lines.push(`<rect x="${mac_cx}" y="${mac_cy - macH / 2}" width="${macW}" height="${macH}" fill="#e74c3c" opacity="0.7" rx="2"/>`);
    texts.push(`<text x="${mac_cx + macW / 2}" y="${mac_cy - 10}" text-anchor="middle" font-family="monospace" font-size="10" fill="#e74c3c">MAC=${mac.toFixed(1)}mm</text>`);
  }

  // Dimension annotations
  if (showDimensions) {
    texts.push(
      `<text x="${ox - cr * s / 2}" y="${oy - 8}" text-anchor="middle" font-family="monospace" font-size="11" fill="#2c3e50">c_r = ${cr}mm</text>`,
      `<text x="${TLE[0] + ct * s / 2}" y="${TLE[1] + 12}" text-anchor="middle" font-family="monospace" font-size="11" fill="#2c3e50">c_t = ${ct}mm</text>`,
      `<text x="${pad + 15}" y="${oy + b * s / 2}" text-anchor="middle" font-family="monospace" font-size="11" fill="#2c3e50" transform="rotate(-90,${pad + 15},${oy + b * s / 2})">b = ${b}mm</text>`,
      `<text x="${pad}" y="${oy + b * s + 18}" text-anchor="start" font-family="monospace" font-size="11" fill="#7f8c8d">λ = ${taperRatio(wing).toFixed(3)}  |  AR = ${aspectRatio(wing).toFixed(2)}  |  S = ${wingArea(wing).toFixed(0)}mm²  |  sweep = ${sw}°</text>`
    );
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" style="background:#fafafa">
  <title>${title}</title>
  ${lines.join('\n  ')}
  ${texts.join('\n  ')}
</svg>`;
}
