import yaml
import os
import sys

def main():
    folder = '.github/workflows'
    failed = False
    for filename in os.listdir(folder):
        if filename.endswith('.yml'):
            path = os.path.join(folder, filename)
            try:
                with open(path, 'r') as f:
                    yaml.safe_load(f)
                # print(f"✅ {filename} is valid.")
            except yaml.YAMLError as e:
                print(f"❌ {filename} is INVALID:")
                print(e)
                failed = True
    if failed:
        sys.exit(1)
    else:
        print("✅ All YAML files in .github/workflows/ are valid.")

if __name__ == "__main__":
    main()
