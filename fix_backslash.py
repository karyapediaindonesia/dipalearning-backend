import glob

for f in glob.glob('backend/templates/dashboard/pages/*.html'):
    c = open(f, encoding='utf-8').read()
    c_new = c.replace(r"(\'{{", r"('{{")
    c_new = c_new.replace(r"}}\',", r"}}',")
    if c_new != c:
        open(f, 'w', encoding='utf-8').write(c_new)
        print('Fixed backslash:', f)
