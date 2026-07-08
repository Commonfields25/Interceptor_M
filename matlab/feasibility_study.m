%% Interceptor_M — Feasibility & Constraint Study (v2.1)
% Author: Lead Designer (Jules)
% Description: Validates CE01-CE03 constraints for the G3 design baseline.

clear; clc;

%% 1. Baseline Parameters (v2.1.0)
MTOW_target = 0.400;      % kg (DD-400)
m_cad_calculated = 0.3824; % kg (From L3 exports/reports)
g = 9.81;

% Design Loads
G_limit = 15.1;
G_ultimate = 22.7; % 1.5x FS

% Geometry
max_tube_bore = 40.0; % mm
fuselage_dia = 35.0;  % mm

%% 2. [CE03] Mass & Propulsion Feasibility
m_margin = MTOW_target - m_cad_calculated;
margin_pct = (m_margin / MTOW_target) * 100;

fprintf('--- [CE03] Mass Feasibility ---\n');
fprintf('Target MTOW: %.3f kg\n', MTOW_target);
fprintf('CAD Calculated Mass: %.3f kg\n', m_cad_calculated);
fprintf('Current Margin: %.1f g (%.1f%%)\n', m_margin*1000, margin_pct);

if m_cad_calculated <= MTOW_target
    fprintf('STATUS: PASS\n');
else
    fprintf('STATUS: FAIL - Vehicle overweight.\n');
end

%% 3. [CE01] Structural / Launcher Interface
F_ultimate = m_cad_calculated * G_ultimate * g;

fprintf('\n--- [CE01] Structural Feasibility (Launch) ---\n');
fprintf('Ultimate Design Force (22.7G): %.1f N\n', F_ultimate);

% Sabot interface check (ASA material)
sigma_yield_asa = 35e6; % Pa
A_contact_sabot = pi * ((40/1000/2)^2 - (35/1000/2)^2); % m^2
sigma_actual = F_ultimate / A_contact_sabot;

fprintf('Sabot Interface Pressure: %.2f MPa\n', sigma_actual / 1e6);
if sigma_actual < sigma_yield_asa
    fprintf('STATUS: PASS\n');
else
    fprintf('STATUS: FAIL\n');
end

%% 4. [CE02] Geometric Clearance
clearance = (max_tube_bore - fuselage_dia) / 2;
fprintf('\n--- [CE02] Geometric Feasibility ---\n');
fprintf('Radial Clearance: %.1f mm\n', clearance);
if abs(clearance - 2.5) < 0.1
    fprintf('STATUS: PASS (Target 2.5mm met)\n');
else
    fprintf('STATUS: WARNING (Check sabot tolerances)\n');
end

fprintf('\n--- CONCLUSION ---\n');
if m_margin >= 0
    fprintf('FEASIBILITY: GO (G3 Baseline Validated)\n');
else
    fprintf('FEASIBILITY: NO-GO\n');
end
