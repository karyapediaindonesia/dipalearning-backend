import glob
import re

for f in glob.glob('backend/templates/dashboard/pages/*.html'):
    c = open(f, encoding='utf-8').read()
    
    # We want to replace unquoted {{ something.id }} in delete function calls
    # Example: onclick="deleteBranch({{ branch.id }}, '{{ branch.name }}')"
    # Regex: onclick="delete([A-Za-z]+)\(\{\{\s*([a-zA-Z0-9_]+)\.id\s*\}\}\s*,
    
    c_new = re.sub(r'onclick="delete([A-Za-z]+)\(\{\{\s*([a-zA-Z0-9_]+)\.id\s*\}\}\s*,',
                   r'onclick="delete\1(\'{{ \2.id }}\',', c)
                   
    if c_new != c:
        open(f, 'w', encoding='utf-8').write(c_new)
        print('Fixed unquoted ID in delete button:', f)
