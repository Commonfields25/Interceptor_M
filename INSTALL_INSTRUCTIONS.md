# Installation Instructions: Interceptor_M Mechanical Engineering Environment

## 1. Core Environment (Recommended)
To avoid dependency conflicts with binary CAD libraries (OCP), it is strongly recommended to use **Conda** or **Mamba**:

```bash
# Create and activate environment
mamba create -n interceptor_cad python=3.11 build123d
mamba activate interceptor_cad
```

## 2. Install CAD Libraries & Industrial Warehouses
Once the environment is active, install the necessary L3 engineering extensions:

```bash
pip install bd_warehouse bd_vslot PyYAML
```

## 3. Web & Engineering Backend
Install standard project dependencies:

```bash
pip install -r requirements.txt
```

## 4. IDE Recommendation
For real-time 3D feedback while coding parts:
- **VS Code** with the **OCP CAD Viewer** extension.
- **CQ-Editor**: Dedicated IDE for Build123d.

## 5. Development Verification
Run the following to ensure your environment is manufacturing-ready:

```bash
PYTHONPATH=. python3 scripts/verify_assembly_fit.py
```

---
*Standards maintained by Jules for Interceptor_M G3.*
