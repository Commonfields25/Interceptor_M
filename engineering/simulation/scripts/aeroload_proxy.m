function [CL, CD, CM, summary] = aeroload_proxy(alpha_deg, mach, varargin)
%AEROLOAD_PROXY  Aerodynamic load proxy (lift/drag/moment)
%   Compatible with GNU Octave 8.x+ and MATLAB R2023b+
%   Based on D2_aerodynamics.md + PARAMETERS.json v1.0.2 (DD platform)
%
%  SYNOPSIS
%    aeroload_proxy(alpha_deg, mach)
%    aeroload_proxy(alpha_deg, mach, platform)
%    [CL, CD, CM] = aeroload_proxy(...)
%
%  INPUTS
%    alpha_deg : Angle of attack [degrees]
%    mach      : Mach number
%    platform  : 'DD' (default), 'DI', or 'DC'
%
%  AERODYNAMIC MODEL (DD platform)
%    Fuselage  : 380 mm × 200 mm × 100 mm, Ø35mm
%    Wing      : 4 × delta wings, span=110mm, chord=60mm, sweep=45°
%    Tail      : 4 × cruciform, span=75mm, chord=40mm, sweep=40°
%    Wing area : 4 × (0.11 × 0.06/2) = 13.2 cm²
%    Ref area  : 0.0132 m²
%    Airfoil   : NACA 0004 (symmetric, t/c=0.04)
%
%  OUTPUT
%    CL       : Lift coefficient (vector, scalar, or NaN at stall)
%    CD       : Drag coefficient
%    CM       : Pitch moment coefficient (about quarter-chord)
%    summary  : Struct with geometry, derivatives, stall info

  %% 1. Input parsing
  if nargin < 2
    error('aeroload_proxy: requires alpha_deg and mach');
  end
  if nargin >= 3 && ~isempty(varargin{1}); platform = varargin{1}; else platform = 'DD'; end

  %% 2. Geometry by platform (from PARAMETERS.json v1.0.2)
  switch upper(platform)
    case 'DD'
      L_fus = 0.380; W_fus = 0.200; H_fus = 0.100;
      span_w = 0.110; chord_w = 0.060;
      span_t = 0.075; chord_t = 0.040;
      sweep_w = 45; sweep_t = 40;
      mtow = 0.400;  % kg
      S_ref = 4 * (span_w * chord_w / 2);  % 0.0132 m²
    case 'DI'
      L_fus = 0.365; W_fus = 0.180; H_fus = 0.090;
      span_w = 0.135; chord_w = 0.060;
      span_t = 0.075; chord_t = 0.040;
      sweep_w = 45; sweep_t = 40;
      mtow = 0.300;
      S_ref = 4 * (span_w * chord_w / 2);
    case 'DC'
      L_fus = 0.350; W_fus = 0.160; H_fus = 0.080;
      span_w = 0.120; chord_w = 0.060;
      span_t = 0.075; chord_t = 0.040;
      sweep_w = 45; sweep_t = 40;
      mtow = 0.250;
      S_ref = 4 * (span_w * chord_w / 2);
    otherwise
      error('aeroload_proxy: unknown platform ''%s''', platform);
  end

  %% 3. Wing aero coefficients (DATCOM-style, thin airfoil theory)
  alpha   = alpha_deg * pi / 180;  % [rad]
  t_c     = 0.04;                  % NACA 0004
  sweep   = sweep_w * pi / 180;
  AR      = (span_w^2) / S_ref;   % Aspect ratio
  e       = 0.90;                  % Oswald efficiency (delta wing est.)

  % --- Lift slope (2D thin airfoil, corrected for finite span) ---
  alpha_2D = 2 * pi * alpha;        % thin airfoil theory
  CL_2D_w  = alpha_2D;              % per rad

  % Prandtl-Glauert compressibility correction
  if mach < 0.95
    beta_PG = sqrt(max(1 - mach^2, 1e-6));
    CL_2D_w = CL_2D_w / beta_PG;
  else
    % Transonic / supersonic — use Ackeret for first approx
    CL_2D_w = 4 * alpha * mach / sqrt(mach^2 - 1);
  end

  % Finite-wing lift slope
  CLa = CL_2D_w * AR / (AR + 2);    % per rad

  % Lift curve (linear portion, stall near 15° alpha)
  alpha_stall_deg = 15;
  alpha_stall     = alpha_stall_deg * pi / 180;
  CL_max_2D       = 2 * pi * alpha_stall;
  CL_max          = CL_max_2D * AR / (AR + 2);

  if abs(alpha_deg) <= alpha_stall_deg
    CL = CLa * alpha;
  else
    CL = NaN;  % stall regime — not modelled
  end

  %% 4. Drag coefficient (polar CD = CD0 + K*CL^2)
  % Friction drag from D2
  Sw = pi * 0.035 * L_fus;          % wetted area fuselage
  Cf = 0.0032;                      % turbulent flat plate (Re~3e6)
  S_wet = 1.2 * Sw;                 % wetted area correction
  CD_f = Cf * S_wet / S_ref;        % friction drag

  % Pressure drag (Mach-dependent, from D2 table at alpha=0)
  if mach < 0.8
    CD_press = 0.047 - CD_f;
  elseif mach < 1.5
    CD_press = 0.064 - CD_f;
  else
    CD_press = 0.095 - CD_f;
  end
  CD_press = max(CD_press, 0.005);  % floor

  % Induced drag (finite wing)
  K = 1 / (pi * e * AR);

  % Total drag polar
  if isnan(CL)
    CD = CD_f + CD_press + 0.3 * CL_max^2 * K;  % post-stall estimate
  else
    CD = CD_f + CD_press + K * CL^2;
  end

  %% 5. Pitch moment (about quarter-chord, symmetric airfoil → Cm0 ≈ 0)
  Cm = -0.1 * CL;   % pitch-down moment coupling (static stability derivative)

  %% 6. Summary struct
  summary = struct();
  summary.platform     = platform;
  summary.mach         = mach;
  summary.alpha_deg    = alpha_deg;
  summary.S_ref_m2     = S_ref;
  summary.AR           = AR;
  summary.CL           = CL;
  summary.CD           = CD;
  summary.CM           = Cm;
  summary.CD0          = CD_f + CD_press;
  summary.CL_max       = CL_max;
  summary.alpha_stall  = alpha_stall_deg;
  summary.mtow_kg      = mtow;
  summary.L_fus_m      = L_fus;

  %% 7. Print
  fprintf('\n');
  fprintf('========================================\n');
  fprintf('  AEROLOAD PROXY — %s Platform\n', platform);
  fprintf('========================================\n');
  fprintf('  Mach      : %.2f\n', mach);
  fprintf('  Alpha     : %.1f deg\n', alpha_deg);
  fprintf('  Wing Area : %.4f m²\n', S_ref);
  fprintf('  Aspect R. : %.2f\n', AR);
  fprintf('----------------------------------------\n');
  fprintf('  CL        : %.4f%s\n', CL, ternary(isnan(CL), ' [STALL]', ''));
  fprintf('  CD        : %.4f\n', CD);
  fprintf('  L/D       : %.2f\n', CL / CD);
  fprintf('  CM        : %.4f\n', Cm);
  fprintf('  CD0       : %.4f\n', CD_f + CD_press);
  fprintf('  CL_max    : %.4f @ %.0f deg\n', CL_max, alpha_stall_deg);
  fprintf('========================================\n');

  %% Helper (Octave/MATLAB compatible inline)
  function y = ternary(cond, a, b)
    if cond; y = a; else; y = b; end
  end
end
