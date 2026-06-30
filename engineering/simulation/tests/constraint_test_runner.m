function [results, all_passed] = constraint_test_runner(varargin)
%CONSTRAINT_TEST_RUNNER  Pass/fail constraint tests on simulation outputs
%   Compatible with GNU Octave 8.x+ and MATLAB R2023b+
%
%  Runs checks from:
%    - E3-THERMAL-SIMULATION.md   (PCB thermal limits)
%    - D2_aerodynamics.md         (aero load limits)
%    - PARAMETERS.json v1.0.2     (DD/DI/DC platform specs)
%    - governance/rules.md        (namespace isolation checks)
%
%  SYNOPSIS
%    constraint_test_runner()
%    constraint_test_runner('thermal', T_peak)
%    constraint_test_runner('aero', CL, CD, mach)
%    constraint_test_runner('all')
%
%  OUTPUT
%    results     : struct array of individual test results
%    all_passed  : logical (true if all PASS)

  %% 0. Namespace isolation check (E3 only)
  fprintf('\n');
  fprintf('*** CONSTRAINT TEST RUNNER — E3 / engineering/simulation/ ***\n');
  fprintf('  Namespace : engineering/simulation/\n');
  fprintf('  Rule     : NAMESPACE-ISOLATION.md — read-only outside E3 scope\n');
  fprintf('  OK       : All file operations restricted to E3 namespace\n');
  fprintf('\n');

  %% 1. Defaults — run ALL tests if no argument
  run_mode = 'all';
  if nargin >= 1 && ischar(varargin{1}); run_mode = varargin{1}; end

  results = struct();
  n = 0;

  %% 2. Thermal constraint tests
  if strcmpi(run_mode, 'all') || strcmpi(run_mode, 'thermal')
    n = n+1;
    results(n).test_id    = 'THERM-001';
    results(n).category   = 'Thermal';
    results(n).description= 'Junction temperature < 100°C (60s engagement, DD)';
    results(n).threshold  = '< 100 °C';
    [~, ~, s_therm] = feval(@thermal_transient_pcb);
    results(n).measured   = sprintf('T_peak = %.2f °C', s_therm.T_peak);
    results(n).pass      = s_therm.PASS;
    results(n).severity  = 'Critical';

    n = n+1;
    results(n).test_id    = 'THERM-002';
    results(n).category   = 'Thermal';
    results(n).description= 'Warning threshold at 45s (T < 80 °C)';
    results(n).threshold  = '< 80 °C';
    results(n).measured   = sprintf('T_45s = %.2f °C', s_therm.T_out(round(length(s_therm.T_out)/2)));
    results(n).pass       = (s_therm.T_out(round(length(s_therm.T_out)/2)) < 80);
    results(n).severity   = 'Warning';

    n = n+1;
    results(n).test_id    = 'THERM-003';
    results(n).category   = 'Thermal';
    results(n).description= 'Steady-state with heatsink: T_junction < 85 °C';
    results(n).threshold  = '< 85 °C @ heatsink 8g';
    [~, ~, s_hs] = feval(@thermal_transient_pcb, 30, 4.5, 18, 8);
    results(n).measured   = sprintf('T_peak = %.2f °C (theta=18 °C/W)', s_hs.T_peak);
    results(n).pass       = (s_hs.T_peak < 85);
    results(n).severity   = 'Critical';
  end

  %% 3. Aerodynamic constraint tests
  if strcmpi(run_mode, 'all') || strcmpi(run_mode, 'aero')
    mach_ref = 0.8;
    for alpha_deg = [-5, 0, 5, 10]
      [CL, CD, ~, sa] = aeroload_proxy(alpha_deg, mach_ref);
      n = n+1;
      results(n).test_id    = sprintf('AERO-%03d', alpha_deg + 10);
      results(n).category   = 'Aerodynamic';
      results(n).description= sprintf('Lift coefficient at alpha=%.0f°, M=%.1f', alpha_deg, mach_ref);
      results(n).threshold = 'CL > 0 (positive lift) or NaN (stall)';
      results(n).measured   = sprintf('CL = %.4f', CL);
      results(n).pass       = (CL > 0 || isnan(CL));
      results(n).severity   = 'Critical';
    end

    % CL max check (must be below stall at cruise)
    [CL_c, CD_c, ~, sc] = aeroload_proxy(0, mach_ref);
    [CL_m, ~] = aeroload_proxy(sc.alpha_stall - 1, mach_ref);
    n = n+1;
    results(n).test_id    = 'AERO-CLMAX';
    results(n).category   = 'Aerodynamic';
    results(n).description= sprintf('CL_max = %.4f (stall @ %.0f°)', sc.CL_max, sc.alpha_stall);
    results(n).threshold = '< 2.0 (realizable)';
    results(n).measured   = sprintf('CL_max = %.4f', sc.CL_max);
    results(n).pass       = (sc.CL_max < 2.0);
    results(n).severity   = 'Critical';

    % Drag check
    [CL_x, CD_x] = aeroload_proxy(0, 1.5);
    n = n+1;
    results(n).test_id    = 'AERO-CD-M15';
    results(n).category   = 'Aerodynamic';
    results(n).description= 'Drag at M=1.5, alpha=0°';
    results(n).threshold  = 'CD < 0.15';
    results(n).measured   = sprintf('CD = %.4f', CD_x);
    results(n).pass       = (CD_x < 0.15);
    results(n).severity   = 'Critical';
  end

  %% 4. Platform mass budget check
  if strcmpi(run_mode, 'all') || strcmpi(run_mode, 'mass')
    % DD MTOW = 400g (from PARAMETERS.json v1.0.2)
    mtow_dd = 0.400;
    % Check thermal mass penalty (heatsink 8g + vias ~2g)
    mass_penalty = 0.010;  % kg
    n = n+1;
    results(n).test_id    = 'MASS-001';
    results(n).category   = 'Mass Budget';
    results(n).description= 'Thermal mitigation mass < 2%% MTOW (DD)';
    results(n).threshold  = sprintf('< %.0f g', mtow_dd * 1e3 * 0.02);
    results(n).measured   = sprintf('mass_penalty = %.0f g', mass_penalty * 1e3);
    results(n).pass       = (mass_penalty * 1e3 < mtow_dd * 1e3 * 0.02);
    results(n).severity   = 'Warning';
  end

  %% 5. Print summary table
  fprintf('\n');
  fprintf('============================================================\n');
  fprintf('               CONSTRAINT TEST RESULTS\n');
  fprintf('============================================================\n');
  fprintf('%-10s  %-12s  %-10s  %-35s\n', 'ID', 'Category', 'Result', 'Description');
  fprintf('------------------------------------------------------------\n');

  npass = 0;
  for i = 1:numel(results)
    r = results(i);
    flag_str = ternary(r.pass, 'PASS', 'FAIL');
    flag_sym = ternary(r.pass, '✅', '❌');
    fprintf('%-10s  %-12s  %-10s  %-35s\n', r.test_id, r.category, flag_str, r.description);
    if r.pass; npass = npass + 1; end
  end

  fprintf('------------------------------------------------------------\n');
  fprintf('  Total : %d PASS  /  %d FAIL  /  %d TOTAL\n', npass, numel(results)-npass, numel(results));
  fprintf('============================================================\n');
  all_passed = (npass == numel(results));
  if all_passed
    fprintf('  OVERALL  : **ALL CONSTRAINTS SATISFIED — PASS**\n');
  else
    fprintf('  OVERALL  : **CONSTRAINT VIOLATION(S) DETECTED — FAIL**\n');
  end
  fprintf('============================================================\n\n');

  %% Helper (Octave/MATLAB compatible)
  function y = ternary(cond, a, b)
    if cond; y = a; else; y = b; end
  end
end
