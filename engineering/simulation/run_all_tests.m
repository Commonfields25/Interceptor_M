% run_all_tests.m
% Dual-stack (GNU Octave / MATLAB) simulation orchestrator
% Interceptor_M — engineering/simulation/
% ISO: ISO9001 §9.1 | ISO15288 §5.3.2.6
%
% Runs: thermal, aeroload, constraint tests, plots
% Exit: 0 = all PASS, non-zero = one or more FAIL

function run_all_tests()
  fprintf('[run_all_tests] Octave/MATLAB dual-stack test runner\n');
  fprintf('Octave/MATLAB version: %s\n', version());

  passed = 0;
  failed = 0;
  results = struct();

  %% Thermal transient
  fprintf('\n=== TEST: thermal_transient_pcb ===\n');
  try
    addpath(fullfile(fileparts(mfilename('fullpath')), 'scripts'));
    if exist('thermal_transient_pcb','file') == 2
      [~, ~, summ] = thermal_transient_pcb();
      if summ.PASS
        fprintf('PASS: thermal_transient_pcb (T_peak=%.2f C)\n', summ.T_peak);
        passed = passed + 1;
        results.thermal = 'PASS';
      else
        fprintf(2, 'FAIL: thermal_transient_pcb (T_peak=%.2f C exceeds limit)\n', summ.T_peak);
        failed = failed + 1;
        results.thermal = 'FAIL';
      end
    else
      fprintf(2, 'FAIL: thermal_transient_pcb.m not in path\n');
      failed = failed + 1;
      results.thermal = 'FAIL';
    end
  catch err
    fprintf(2, 'FAIL: thermal_transient_pcb threw: %s\n', err.message);
    failed = failed + 1;
    results.thermal = 'FAIL';
  end

  %% Aeroload proxy
  fprintf('\n=== TEST: aeroload_proxy ===\n');
  try
    addpath(fullfile(fileparts(mfilename('fullpath')), 'scripts'));
    if exist('aeroload_proxy','file') == 2
      [CL, CD, ~, summ] = aeroload_proxy(5, 0.2);
      if ~isnan(CL) && CL > 0 && CD < 0.15
        fprintf('PASS: aeroload_proxy (CL=%.4f, CD=%.4f)\n', CL, CD);
        passed = passed + 1;
        results.aeroload = 'PASS';
      else
        fprintf(2, 'FAIL: aeroload_proxy out of envelope (CL=%.4f, CD=%.4f)\n', CL, CD);
        failed = failed + 1;
        results.aeroload = 'FAIL';
      end
    else
      fprintf(2, 'FAIL: aeroload_proxy.m not in path\n');
      failed = failed + 1;
      results.aeroload = 'FAIL';
    end
  catch err
    fprintf(2, 'FAIL: aeroload_proxy threw: %s\n', err.message);
    failed = failed + 1;
    results.aeroload = 'FAIL';
  end

  %% Constraint test runner
  fprintf('\n=== TEST: constraint_test_runner ===\n');
  try
    addpath(fullfile(fileparts(mfilename('fullpath')), 'tests'));
    addpath(fullfile(fileparts(mfilename('fullpath')), 'scripts'));
    if exist('constraint_test_runner','file') == 2
      [~, all_passed] = constraint_test_runner();
      if all_passed
        fprintf('PASS: constraint_test_runner\n');
        passed = passed + 1;
        results.constraints = 'PASS';
      else
        fprintf(2, 'FAIL: constraint_test_runner returned FAIL\n');
        failed = failed + 1;
        results.constraints = 'FAIL';
      end
    else
      fprintf(2, 'FAIL: constraint_test_runner.m not in path\n');
      failed = failed + 1;
      results.constraints = 'FAIL';
    end
  catch err
    fprintf(2, 'FAIL: constraint_test_runner threw: %s\n', err.message);
    failed = failed + 1;
    results.constraints = 'FAIL';
  end

  %% Summary
  fprintf('\n========================================\n');
  fprintf('SUMMARY: %d PASS, %d FAIL\n', passed, failed);
  fprintf('results = \n');
  disp(results);
  fprintf('========================================\n');

  if failed > 0
    fprintf(2, 'OVERALL: FAIL\n');
    error('One or more tests failed');
  else
    fprintf('OVERALL: PASS\n');
  end
end
