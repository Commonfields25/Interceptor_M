%% Interceptor_M — Feasibility & Constraint Study (v1.6)
% Author: Lead Designer (Jules)
% Description: Evaluates the project feasibility across structural,
% aerodynamic, and mass constraints for the DD line.

clear; clc;

%% 1. Input Parameters (v1.6 Baseline)
MTOW_target = 0.400;      % kg (400g)
m_structure_v16 = 0.336;  % kg (From BOM Baseline v1.5/1.6)
g = 9.81;                 % m/s^2

% Constraints from Cahier_Charges_Prototype.md
G_maneuver_req = 25;      % Required maneuver load
FS = 1.5;                 % Factor of Safety
max_tube_dia = 40;        % mm
fuselage_dia = 35;        % mm

%% 2. Mass Margin Analysis
m_avail_payload = MTOW_target - m_structure_v16;
margin_pct = (m_avail_payload / MTOW_target) * 100;

fprintf('--- Mass Feasibility ---\n');
fprintf('Target MTOW: %.3f kg\n', MTOW_target);
fprintf('Current Structure Mass (v1.6): %.3f kg\n', m_structure_v16);
fprintf('Available Payload/Propulsion: %.3f kg\n', m_avail_payload);
fprintf('Margin: %.1f%%\n', margin_pct);

if m_avail_payload < 0.050
    fprintf('STATUS: CRITICAL - Insufficient margin for propulsion and seekers.\n');
else
    fprintf('STATUS: PASS\n');
end

%% 3. Structural Feasibility (Launch Force)
launch_accel_target = 25; % g
F_launch = m_structure_v16 * launch_accel_target * g; % Newton
F_ultimate = F_launch * FS;

fprintf('\n--- Structural Feasibility (Launch) ---\n');
fprintf('Target Launch Accel: %d g\n', launch_accel_target);
fprintf('Peak Launch Force: %.1f N\n', F_launch);
fprintf('Ultimate Design Force (FS=1.5): %.1f N\n', F_ultimate);

% Simple stress check placeholder for SABOT-001 (ASA material)
sigma_yield_asa = 35e6; % Pa (Approx 35 MPa)
A_contact_sabot = pi * ((max_tube_dia/1000/2)^2 - (fuselage_dia/1000/2)^2); % m^2
sigma_actual = F_ultimate / A_contact_sabot;

fprintf('Sabot Interface Pressure: %.2f MPa\n', sigma_actual / 1e6);
if sigma_actual < sigma_yield_asa
    fprintf('STATUS: PASS (Material Strength > Load)\n');
else
    fprintf('STATUS: FAIL (Material failure likely)\n');
end

%% 4. Geometric Constraint (Launcher Clearance)
clearance = (max_tube_dia - fuselage_dia) / 2;
fprintf('\n--- Geometric Feasibility ---\n');
fprintf('Radial Clearance (Tube-Fuselage): %.1f mm\n', clearance);
if clearance >= 2.5
    fprintf('STATUS: PASS (Sufficient for SABOT-001)\n');
else
    fprintf('STATUS: WARNING (Tight tolerances required)\n');
end

fprintf('\n--- CONCLUSION ---\n');
if margin_pct < 20
    fprintf('FEASIBILITY: AT RISK (Mass budget needs optimization)\n');
else
    fprintf('FEASIBILITY: GO\n');
end
