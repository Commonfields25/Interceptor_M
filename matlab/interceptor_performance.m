%% Interceptor_M — Technical Performance Baseline (DD-400)
% Author: Jules (Physics Expert)
% Description: This script calculates the theoretical performance limits
% for the 400g / 380mm Defense Interceptor (DD).
% Verified against simulation/constants.py

clear; clc;

%% 1. Parameters (Unified Baseline)
m = 0.400;              % kg
g = 9.80665;            % m/s^2
rho = 1.225;            % kg/m^3 (Sea Level)
S_ref = 0.001;          % m^2
Cl_alpha = 2.0;         % per rad
Cd0 = 0.35;             % Drag coefficient
max_g_limit = 25.0;     % Structural/Actuator Limit
thrust_max = 12.0;      % N (SC-02)

%% 2. Performance Calculations
V_target = 300;         % Intercept Speed (m/s)
q = 0.5 * rho * V_target^2;

% A. Load Factor at 12 deg Angle of Attack
alpha_rad = deg2rad(12);
L = q * S_ref * Cl_alpha * alpha_rad;
n_aero = L / (m * g);
n_actual = min(n_aero, max_g_limit);

% B. Turn Radius
R_min = V_target^2 / (n_actual * g);

% C. Drag at Intercept
D = q * S_ref * Cd0;

fprintf('--- Interceptor_M DD-400 MATLAB Verification ---\n');
fprintf('Aero-limited Load Factor (12 deg AoA): %.1f g\n', n_aero);
fprintf('Minimum Turn Radius (at 300 m/s): %.1f m\n', R_min);
fprintf('Intercept Drag (300 m/s): %.2f N\n', D);
fprintf('Thrust-to-Weight Ratio: %.2f\n', thrust_max / (m * g));
fprintf('------------------------------------------------\n');
