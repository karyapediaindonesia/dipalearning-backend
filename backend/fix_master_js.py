import os, re

path = r'c:\Users\PC-HMK\Desktop\Project\dipalearning\backend\templates\dashboard\pages'

print("=== Fixing JS AJAX data wrapper in Master Templates ===")

for file in os.listdir(path):
    if file.startswith('master-') and file.endswith('.html'):
        filepath = os.path.join(path, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix $.get
        # From: $.get(..., function(data) {
        # To: $.get(..., function(response) { const data = response.data || response;
        new_content = re.sub(
            r'\$\.get\(([^,]+),\s*function\(data\)\s*\{',
            r'$.get(\1, function(response) {\n            const data = response.data || response;',
            content
        )
        # Fix $.get with res
        new_content = re.sub(
            r'\$\.get\(([^,]+),\s*function\(res\)\s*\{',
            r'$.get(\1, function(response) {\n            const res = response.data || response;',
            new_content
        )
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed $.get in {file}")
