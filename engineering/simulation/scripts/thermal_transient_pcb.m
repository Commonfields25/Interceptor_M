function [t_out, T_out, summary] = thermal_transient_pcb(varargin)
%THERMAL_TRANSIENT_PCB  60-second transient PCB thermal analysis
%   Compatible with GNU Octave 8.x+ and MATLAB R2023b+
%   Based on E3-THERMAL-SIMULATION.md (DD platform, 400g, 11.1V)
%
%  SYNOPSIS
%    thermal_transient_pcb()
%    thermal_transient_pcb(T_amb, P_total, theta_JA, mass_hs, dt)
%
%  PARAMETERS (DD platform defaults)
%    T_amb    : Ambient temperature [°C]  (default 30)
%    P_total  : Total power dissipation [W] (default 4.5, duty-cycled)
%    theta_JA : Thermal resistance [°C/W]  (default 25, no heatsink)
%              With 8g Al heatsink: ~18 °C/W
%    mass_hs  : Heatsink mass [g] (default 8)
%    dt       : Timestep [s] (default 0.5)
%
%  OUTPUT
%    t_out    : Time vector [s]
%    T_out    : Junction temperature vector [°C]
%    summary  : Struct with peak, final, margin, PASS/FAIL

  %% 1. Input parsing (Octave/MATLAB compatible)
  if nargin >= 1 && ~isempty(varargin{1}); T_amb = varargin{1}; else T_amb = 30; end
  if nargin >= 2 && ~isempty(varargin{2}); P_total = varargin{2}; else P_total = 4.5; end
  if nargin >= 3 && ~isempty(varargin{3}); theta_JA = varargin{3}; else theta_JA = 25; end
  if nargin >= 4 && ~isempty(varargin{4}); mass_hs = varargin{4}; else mass_hs = 8; end
  if nargin >= 5 && ~isempty(varargin{5}); dt = varargin{5}; else dt = 0.5; end

  %% 2. Thermal model — lumped RC (1st-order ODE)
  %   dT/dt = (P - (T - T_amb) / theta_JA) / C_th
  %   C_th ~ 10 J/°C for 30x30mm PCB + component mass

  C_th = 10;  % [J/°C] — thermal capacitance estimate
  t_max = 60; % [s]
  nSteps = round(t_max / dt) + 1;
  t_out  = linspace(0, t_max, nSteps)';
  T_out  = zeros(nSteps, 1);

  T_out(1) = T_amb;
  for i = 2:nSteps
    dT = (P_total - (T_out(i-1) - T_amb) / theta_JA) / C_th;
    T_out(i) = T_out(i-1) + dT * dt;
  end

  %% 3. Thermal limit & duty-cycling check
  T_limit  = 100;  % °C — junction limit
  T_warn   = 80;   % °C — warning threshold
  T_peak   = max(T_out);
  T_final  = T_out(end);
  margin   = T_limit - T_peak;

  summary = struct();
  summary.T_amb      = T_amb;
  summary.P_total    = P_total;
  summary.theta_JA   = theta_JA;
  summary.mass_hs    = mass_hs;
  summary.dt         = dt;
  summary.t_duration = t_max;
  summary.T_peak     = T_peak;
  summary.T_final    = T_final;
  summary.T_warn     = T_warn;
  summary.T_limit    = T_limit;
  summary.margin_C   = margin;
  summary.PASS       = (T_peak <= T_limit);

  %% 4. Print summary
  fprintf('\n');
  fprintf('========================================\n');
  fprintf('  THERMAL TRANSIENT PCB — DD Platform\n');
  fprintf('  Platform    : Defense Deployable (DD)\n');
  fprintf('  MTOW        : 400 g\n');
  fprintf('  Bus Voltage : 11.1 V (3S LiPo)\n');
  fprintf('========================================\n');
  fprintf('  Ambient       : %.1f °C\n', T_amb);
  fprintf('  Power (eff.) : %.2f W\n', P_total);
  fprintf('  Theta_JA      : %.1f °C/W\n', theta_JA);
  fprintf('  Heatsink mass: %.1f g\n', mass_hs);
  fprintf('  Duration     : %.0f s\n', t_max);
  fprintf('----------------------------------------\n');
  fprintf('  Peak T_junc  : %.2f °C\n', T_peak);
  fprintf('  Final T_junc : %.2f °C\n', T_final);
  fprintf('  Warning @    : %.0f °C\n', T_warn);
  fprintf('  Limit @      : %.0f °C\n', T_limit);
  fprintf('  Margin       : %.2f °C\n', margin);
  fprintf('----------------------------------------\n');
  if T_peak > T_limit
    fprintf('  RESULT       : **FAIL**  (peak exceeds %.0f °C)\n', T_limit);
  elseif T_peak > T_warn
    fprintf('  RESULT       : **PASS with WARNING**\n');
  else
    fprintf('  RESULT       : **PASS**\n');
  end
  fprintf('========================================\n');
  fprintf('\n');
end
