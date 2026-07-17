import os

BASE_DIR = r"c:\dipalearning\backend"

replacements = {
    "folder_name = \"dompet\"": "folder_name = \"dashboard\"",
    "dz_array.pagelevel.dashboard": "dz_array.pagelevel.dashboard",
    "\"dompet\":{#AppName": "\"dashboard\":{#AppName",
    "'dashboard':{#AppName": "'dashboard':{#AppName",
    "Dipa Learning Center": "Dipa Learning Center",
    "": "",
}

for root, dirs, files in os.walk(BASE_DIR):
    if '.git' in root or 'venv' in root or '__pycache__' in root:
        continue

    for file in files:
        if file.endswith('.py') or file.endswith('.html') or file.endswith('.js') or file.endswith('.css'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = content
                for old_str, new_str in replacements.items():
                    new_content = new_content.replace(old_str, new_str)

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed remaining references in: {file_path}")
            except Exception as e:
                pass

print("Done.")
