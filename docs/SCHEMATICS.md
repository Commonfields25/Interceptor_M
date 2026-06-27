---
title: Engineering Schematics & Traceability
---

> **⚠ Notice — Conceptual / Traceability Only**  
> All diagrams below are abstract process and architecture schematics for program traceability, documentation, and governance purposes. They do **not** contain fabrication dimensions, launcher details, weaponization steps, or actionable construction instructions. Treat as internal engineering documentation.

---

## 1 · Roadmap Claims Traceability Lifecycle

```mermaid
flowchart TD
    A([📋 Roadmap Claim]) --> B{Claim Type}
    B -->|Technical Feature| C[Claim in PROTOTYPE_ROADMAP.md]
    B -->|Simulation| D[Claim in simulation/sim_6dof.py]
    B -->|ML Capability| E[Claim in engineering/ML/...]
    B -->|Structural| F[Claim in PRODUCT-FAMILY.md / FEA plan]
    B -->|Governance| G[Claim in OPERATIONS_WORKFLOW*.md]
    C --> H{Traceable to Existing File?}
    D --> H
    E --> H
    F --> H
    G --> H
    H -->|Yes| I[Evidence Path Listed]
    H -->|No| J[Gaps Report Logged]
    I --> K{Gate Review G1/G2/G3}
    J --> K
    K -->|Pass| L([✅ Claim Validated])
    K -->|Fail| M([🔁 Rework / Rescope])
    K -->|Deferred| N([📅 Deferred to Next Phase])
    style L fill:#b8e994
    style M fill:#ffaaa0
    style N fill:#ffe082
    style J fill:#ffaaa0
```

---

## 2 · MAPPO + Isaac Gym Training Architecture

```mermaid
flowchart LR
    subgraph Setup["A · Scenarios & Configuration"]
        SC["Swarm Scenarios swarm_env.py"]
        CF["MAPPO Config hyperparameters.yaml"]
        SEED["Random Seed experiment.yaml"]
    end
    subgraph Env["B · Environment"]
        IG["Isaac Gym Env GPU"]
        IG_CPU["CPU Fallback NumPy Wrapper"]
    end
    subgraph Rollout["C · Rollout Workers"]
        RW1["Worker 1 Policy πθ"]
        RW2["Worker 2 Policy πθ"]
        RW3["Worker N Policy πθ"]
        RW1 --- RW2 --- RW3
    end
    subgraph Train["D · MAPPO Learner"]
        BUF["Rollout Buffer Trajectories"]
        GA["GAE Advantage Estimation"]
        LSTM["Shared LSTM Encoder"]
        ATTN["Attention Over Agents"]
        PP["PPO Clipping Loss Lπ"]
        VL["Value Head Loss LV"]
        OPT["Adam Optimizer lr → θ"]
    end
    subgraph Eval["E · Evaluation & Artifacts"]
        EVAL["Gym Eval Success Rate"]
        CKPT["Model Checkpoint .pt / .onnx"]
        TB["TensorBoard Logs"]
        TR["Training Report markdown"]
    end
    Setup --> Env
    Env --> Rollout
    Rollout --> Train
    Train --> Eval
    SC -.->|"Isaac Gym GPU"| IG
    CF -.->|"GPU Training"| IG
    SC -.->|"CPU Smoke Test"| IG_CPU
    CF -.->|"Unit / CI Run"| IG_CPU
    style IG fill:#aed6f1,stroke:#2980b9
    style IG_CPU fill:#d5f5e3,stroke:#27ae60
    style Train fill:#f9e79f,stroke:#f39c12
    style EVAL fill:#e8daef,stroke:#8e44ad
```

---

## 3 · Simulation-to-Validation Workflow

```mermaid
flowchart TD
    A([🟢 Baseline Simulation]) --> B[sim_6dof.py 6-DOF Equations]
    B --> C{Keep Trajectories?}
    C -->|keep_traj=False Production| D[Monte Carlo N=10 000]
    C -->|keep_traj=True Debug| E[Single Run Full Trajectory]
    D --> F["Stats: P(kill|intercept) E[Cks] σ"]
    E --> F
    F --> G{Model Validation G1 Gate}
    G -->|Fail| H([🔁 Fix Model Resimulate])
    G -->|Pass| I([✅ Baseline Validated])
    I --> J[MAPPO Policy Inference]
    J --> K{Policy Eval G2 Gate}
    K -->|Fail| L([🔁 Retrain or Rescope])
    K -->|Pass| M([✅ Policy Approved])
    M --> N[Export Artifacts .pt config report]
    N --> O([✅ Ready for Physical Prototype])
    style D fill:#aed6f1,stroke:#2980b9
    style I fill:#b8e994
    style M fill:#b8e994
    style H fill:#ffaaa0
    style L fill:#ffaaa0
    style O fill:#b8e994
```

---

## 4 · FEA / NDC Documentation Workflow

```mermaid
flowchart LR
    subgraph NDC["A · NDC Definition"]
        N1["Product Line PRODUCT-FAMILY.md"]
        N2["DD-NDC Boundary Conditions v0.1"]
        N3["Mass / Geometry PARAMETERS.json"]
    end
    subgraph CAD["B · CAD Placeholder"]
        C1["CAD Models CAD/ (future)"]
        C2["STEP / IGES Export Ready"]
    end
    subgraph FEA["C · FEA Preparation"]
        F1["Mesh Plan engineering/DI/FEA/"]
        F2["BCs Defined boundary_conditions.yaml"]
        F3["Solver Inputs Ansys / Code_Aster Not yet run"]
    end
    subgraph Solve["D · Solver & Review"]
        F4["Solve Stress / Modal / Thermal"]
        F5["Results v1 Post-processing"]
        F6["Design Review G2/G3 Gate"]
    end
    NDC --> CAD --> FEA --> Solve
    N1 -.->|"defines"| N2
    N3 -.->|"constrains"| C2
    F2 -.->|"feeds"| F3
    F4 -.->|"produces"| F5
    style F3 fill:#d5f5e3,stroke:#27ae60
    style F4 fill:#aed6f1,stroke:#2980b9
    style F6 fill:#b8e994
```

---

## 5 · Confidentiality & License Decision Flow

```mermaid
flowchart TD
    START([New Document or Artifact]) --> Q1{Publicly Useful?}
    Q1 -->|Yes| Q2{Contains Technical Data or IP?}
    Q1 -->|No| R1([Internal Only - Not Public])
    Q2 -->|No| L1([Apache 2.0 or MIT Fully Open])
    Q2 -->|Yes| Q3{Commercial Sensitivity?}
    Q3 -->|Low| L2([Business License + Notice Apache + Disclaimer])
    Q3 -->|High| Q4{Regulatory Restrictions?}
    Q4 -->|None| L3([Custom License + Export Review + Counsel])
    Q4 -->|ITAR / EAR| L4([Restricted - No Public Disclosure])
    L1 --> FINAL([Classification Applied + Badge])
    L2 --> FINAL
    L3 --> FINAL
    L4 --> FINAL
    R1 --> FINAL
    FINAL --> COMPLY{Export / ITAR Compliance Check}
    COMPLY -->|Pass| DONE([Ready to Publish / Commit])
    COMPLY -->|Fail| LEGAL([Legal / Export Review Required])
    style R1 fill:#ffe082
    style L4 fill:#ffaaa0
    style LEGAL fill:#ffaaa0
    style DONE fill:#b8e994
```

---

## 6 · Staffing & Compute Responsibility Map

```mermaid
flowchart TD
    subgraph Program["Intercepteur_M Program"]
        subgraph ML["ML / AI Team"]
            E2(["E2 - ML Infra Owner MAPPO / Isaac Gym GPU Budget Holder"])
            D3(["D3 - Defense ML Requirements & Evaluation"])
        end
        subgraph DevOps["Platform & Infrastructure"]
            E1(["E1 - Systems Eng CI / Smoke Tests Tracking Dashboard"])
            E3(["E3 - Electronics HW-in-Loop Telemetry Integration"])
        end
        subgraph MGMT["Program Management"]
            AM(["Agent Manager Gate Reviews Milestone Sign-off"])
            AC(["AC Agent Documentation Compliance Tracking"])
        end
    end
    subgraph Compute["Compute Budget Placeholder"]
        WKS["GPU Workstation Local RTX 4090 ~500 W/slot"]
        CLD["Cloud GPU AWS SageMaker / GCP ~10k GPU-hours/phase"]
        CPU["CPU Farm CI / Smoke / Sim Unlimited"]
    end
    subgraph Tracking["Experiment Tracking"]
        TB["TensorBoard Logs & Metrics"]
        GL["GitHub Issues Milestones"]
        PR["PR Reviews E2 / D3 Sign-off"]
    end
    E2 --> WKS
    E2 --> CLD
    E1 --> CPU
    E1 --> TB
    D3 --> GL
    D3 --> PR
    AM --> GL
    AM --> PR
    style E2 fill:#aed6f1,stroke:#2980b9
    style D3 fill:#aed6f1,stroke:#2980b9
    style TB fill:#e8daef,stroke:#8e44ad
    style WKS fill:#f9e79f
    style CLD fill:#f9e79f
```

---

## 7 · Traceability Matrix Summary

| Roadmap Claim | Evidence File | Status |
|---|---|---|
| 6-DOF simulation baseline | simulation/sim_6dof.py | ✅ Implemented |
| Monte Carlo kill analysis | simulation/sim_6dof.py (simulate_engagement) | ✅ Implemented |
| Isaac Gym swarm env | engineering/ML/isaac_gym/swarm_env.py | ✅ Present (CPU wrapper) |
| MAPPO RL training pipeline | engineering/ML/mappo/ | 📋 Scaffolded |
| Product family / NDC definition | PRODUCT-FAMILY.md | 📋 Documented |
| FEA boundary conditions | engineering/DI/ placeholder | ⚠️ Gaps - CAD/FEA missing |
| Governance gate model | OPERATIONS_WORKFLOW*.md | ✅ Implemented |
| CI / smoke test infrastructure | TBD (E1 planned) | ⚠️ Not yet in repo |
| GPU/cloud budget | TBD (E2/D3) | ⚠️ Placeholder only |

---

## 8 · Quick Reference - File Index

| Purpose | Path |
|---|---|
| Program overview | README.md |
| Governance & gates | OPERATIONS_WORKFLOW_V2.md |
| Baseline simulation | simulation/sim_6dof.py |
| ML training | engineering/ML/mappo/ |
| Isaac Gym env | engineering/ML/isaac_gym/swarm_env.py |
| Product NDC | PRODUCT-FAMILY.md |
| FEA plan placeholder | engineering/DI/ |
| Parameters / mass | PARAMETERS.json |
| Prototype roadmap | PROTOTYPE_ROADMAP.md |
| Bot / agent rules | BOT_GUIDELINES.md, rules.md |
| **This file** | docs/SCHEMATICS.md |

---

*Maintained by: Agent Manager & AC Agent - update when gates pass or scope changes.*
