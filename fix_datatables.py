import glob, re

css_block = '''{% block additional_css %}
<!-- Datatable -->
<link href="{% static 'dashboard/vendor/datatables/css/jquery.dataTables.min.css' %}" rel="stylesheet">
{% endblock %}
'''

language_config = '''{
            language: {
                search:       "Cari:",
                lengthMenu:   "Tampilkan _MENU_ data",
                info:         "Menampilkan _START_-_END_ dari _TOTAL_ data",
                infoEmpty:    "Menampilkan 0 dari 0 data",
                infoFiltered: "(disaring dari _MAX_ total data)",
                zeroRecords:  "Tidak ada data ditemukan.",
                emptyTable:   "Tidak ada data tersedia.",
                paginate: {
                    previous: '<i class="fa fa-angle-double-left"></i>',
                    next:     '<i class="fa fa-angle-double-right"></i>'
                }
            }'''

# Fix CSS
for f in ['backend/templates/dashboard/pages/master-kursus.html', 'backend/templates/dashboard/pages/master-level.html', 'backend/templates/dashboard/pages/master-ruangan.html']:
    content = open(f, encoding='utf-8').read()
    if '{% block additional_css %}' not in content:
        content = content.replace('{% block content %}', css_block + '\n{% block content %}')
        open(f, 'w', encoding='utf-8').write(content)

# Fix DataTable language in all files
for f in glob.glob('backend/templates/dashboard/pages/*.html'):
    content = open(f, encoding='utf-8').read()
    if 'DataTable()' in content:
        content = content.replace('DataTable()', f'DataTable({language_config})')
    elif 'DataTable({' in content:
        if 'language: {' in content:
            # Simple regex to replace the language block
            content = re.sub(r'language:\s*\{[^\}]+\s*paginate:\s*\{[^\}]+\}\s*\}', language_config.split('{', 1)[1].strip(), content, flags=re.DOTALL)
        else:
            content = content.replace('DataTable({', f'DataTable({language_config}, ')
    open(f, 'w', encoding='utf-8').write(content)
