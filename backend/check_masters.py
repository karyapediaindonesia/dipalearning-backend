import os, re

path = r'c:\Users\PC-HMK\Desktop\Project\dipalearning\backend\templates\dashboard\pages'

print("=== Checking Master Templates ===")

for file in os.listdir(path):
    if file.startswith('master-') and file.endswith('.html'):
        with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for join:', ' 
            join_issues = re.findall(r"join:'([^']*)'", content)
            if join_issues:
                print(f"{file}: Found single-quote join filter: {join_issues}")
            
            # Check for view button vs view modal
            view_btns = re.findall(r'onclick="(view[A-Za-z0-9_]*)\(this\)"', content)
            if view_btns:
                modals = re.findall(r'id="(view[A-Za-z0-9_]*Modal)"', content, re.IGNORECASE)
                if not modals:
                    print(f"{file}: Has view button {view_btns} but NO view modal found!")
                else:
                    print(f"{file}: View button ok (Modal: {modals})")
            else:
                pass
                # print(f"{file}: No view buttons found.")
