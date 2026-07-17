import os

css_to_add = """
{% block additional_css %}
<style>
    /* Fix DataTable wrapper layout */
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
    }
</style>
{% endblock %}
"""

files = ['master-ruangan.html', 'master-kursus.html', 'master-level.html']

for f in files:
    path = rf'c:\dipalearning\backend\templates\dashboard\pages\{f}'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if '{% block additional_css %}' not in content:
            # Insert just before {% block content %}
            content = content.replace('{% block content %}', css_to_add + '\n{% block content %}')
            
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
