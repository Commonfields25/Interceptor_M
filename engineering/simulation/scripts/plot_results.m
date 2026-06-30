function plot_results(varargin)
%PLOT_RESULTS  Generate 2D figures for temperature and loads
%   Compatible with GNU Octave 8.x+ and MATLAB R2023b+
%
%  SYNOPSIS
%    plot_results()              — all plots
%    plot_results('thermal')     — thermal only
%    plot_results('aero')        — aero only
%    plot_results('thermal', t, T, 'aero', CL_vec, CD_vec, alpha_vec)
%
%  OUTPUT
%    Two PDF/PNG figure files saved to:
%      fig_thermal_transient.pdf
%      fig_aero_polar.pdf
%
%  NOTES
%    - Uses print() with '-dpdf' (works in Octave + MATLAB)
%    - For PNG: replace '-dpdf' with '-dpng' and '-r150'
%    - No proprietary toolboxes required

  %% 0. Detect environment
  % octave = exist('OCTAVE_VERSION', 'builtin') == 5;
  % pkg_list = {};
  % if octave
  %   pkgs = pkg('list'); for i = 1:numel(pkgs); pkg_list{i} = pkgs{i}.name; end
  % end

  mode = 'all';
  if nargin >= 1 && ischar(varargin{1}); mode = varargin{1}; end

  %% 1. Thermal plot
  if strcmpi(mode, 'all') || strcmpi(mode, 'thermal')
    [t_no_hs, T_no_hs, s_no_hs] = thermal_transient_pcb(30, 4.5, 25, 0);
    [t_hs, T_hs, s_hs]          = thermal_transient_pcb(30, 4.5, 18, 8);

    fig1 = figure('visible', 'off');
    hold on;
    plot(t_no_hs, T_no_hs, 'r-', 'linewidth', 2, 'displayname', 'No heatsink (θ=25°C/W)');
    plot(t_hs,   T_hs,   'b-', 'linewidth', 2, 'displayname', 'Heatsink 8g  (θ=18°C/W)');
    plot([0 t_no_hs(end)], [80 80], 'k--', 'linewidth', 1, 'displayname', 'Warning (80°C)');
    plot([0 t_no_hs(end)], [100 100], 'r--', 'linewidth', 1, 'displayname', 'Limit (100°C)');
    xlabel('Time [s]');
    ylabel('Junction Temperature [°C]');
    title('PCB Thermal Transient — DD Platform (11.1V, 4.5W)');
    legend('location', 'southeast');
    grid on;
    hold off;
    fig1_name = 'fig_thermal_transient.pdf';
    print(fig1, '-dpdf', fig1_name);
    fprintf('  [plot] Saved: %s\n', fig1_name);
    close(fig1);
  end

  %% 2. Aerodynamic polar plot
  if strcmpi(mode, 'all') || strcmpi(mode, 'aero')
    alpha_vec = -10:1:14;
    CL_vec = zeros(size(alpha_vec));
    CD_vec = zeros(size(alpha_vec));
    for i = 1:numel(alpha_vec)
      [CL_vec(i), CD_vec(i)] = aeroload_proxy(alpha_vec(i), 0.8);
    end

    fig2 = figure('visible', 'off');
    subplot(1,2,1);
    plot(alpha_vec, CL_vec, 'b-', 'linewidth', 2);
    xlabel('Angle of Attack [deg]');
    ylabel('C_L');
    title('Lift Curve (M=0.8, DD)');
    grid on;
    hold on;
    plot([-10 14], [0 0], 'k--', 'linewidth', 0.8);
    plot([15 15], [-1 2], 'r--', 'linewidth', 1, 'displayname', 'Stall @ 15°');
    legend('CL', 'Zero-lift', 'Stall', 'location', 'southeast');

    subplot(1,2,2);
    plot(CL_vec, CD_vec, 'r-', 'linewidth', 2);
    xlabel('C_L');
    ylabel('C_D');
    title('Drag Polar (M=0.8, DD)');
    grid on;

    suptitle('Aerodynamic Loads — DD Platform, M=0.8');
    fig2_name = 'fig_aero_polar.pdf';
    print(fig2, '-dpdf', fig2_name);
    fprintf('  [plot] Saved: %s\n', fig2_name);
    close(fig2);
  end
end
