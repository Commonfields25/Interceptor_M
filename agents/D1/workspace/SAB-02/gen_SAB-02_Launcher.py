import json

# Geometry generation for SAB-02_Launcher
with open("SAB-02_Launcher_plan.json", "r") as f:
    metadata = json.load(f)
print(
    f"Generating SAB-02_Launcher with length {metadata['parameters']['result_L_lanceur']}mm"
)
# CAD logic goes here...
