import os
import re

files = [
    'master-cabang.html',
    'master-ruangan.html', 
    'master-kursus.html', 
    'master-level.html',
    'master-hari-libur.html',
    'master-alasan-absen.html',
    'master-metode-bayar.html',
    'master-kategori-biaya.html'
]

pattern = re.compile(r'<style>\s*/\* Fix DataTable wrapper layout \*/.*?</style>', re.DOTALL)

# For master-cabang, it might have other styles inside <style>
# so I should probably just replace the exact CSS text.
css_text_to_remove = """    /* Fix DataTable wrapper layout */
    .dataTables_wrapper .dataTables_paginate {
        float: right;
        clear: both;
        margin-top: 10px;
    }
    .dataTables_wrapper .dataTables_paginate .paginate_button {
        padding: 6px 10px !important;
        white-space: nowrap !important;
        line-height: 1.4 !important;
    }
    /* Pastikan info dan paginate sejajar */
    .dataTables_wrapper .row:last-child {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }"""

for f in files:
    path = rf'c:\dipalearning\backend\templates\dashboard\pages\{f}'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # We can just remove the string itself
        # This leaves <style></style> empty in some cases, so let's clean up empty styles
        content = content.replace(css_text_to_remove, '')
        content = content.replace('<style>\n\n</style>', '')
        content = content.replace('<style>\n</style>', '')
        content = content.replace('<style></style>', '')
        
        # Clean up empty {% block additional_css %}
        content = content.replace('{% block additional_css %}\n\n{% endblock %}', '')
        content = content.replace('{% block additional_css %}\n{% endblock %}', '')
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
