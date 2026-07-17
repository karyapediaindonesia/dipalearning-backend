import os

files = [
    'master-ruangan.html', 
    'master-kursus.html', 
    'master-level.html',
    'master-hari-libur.html',
    'master-alasan-absen.html',
    'master-metode-bayar.html',
    'master-kategori-biaya.html'
]

for f in files:
    path = rf'c:\dipalearning\backend\templates\dashboard\pages\{f}'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if already wrapped
        if 'class="content-body"' not in content:
            parts = content.split('{% block content %}')
            if len(parts) >= 2:
                # We need to find the FIRST {% endblock %} that closes the block content
                # But since there might be other endblocks (e.g., from if/for), wait!
                # Actually, in Django templates, `{% endblock %}` specifically closes a `{% block %}`.
                # `if` uses `{% endif %}`, `for` uses `{% endfor %}`. 
                # So `{% endblock %}` ALWAYS closes a `{% block ... %}`.
                # However, if there are multiple blocks, it's safer to just wrap everything between {% block content %} and the FIRST {% endblock %}?
                # Actually, the FIRST {% endblock %} might close a nested block? No, Django blocks cannot be nested inside each other!
                # Ah, they can't be nested. So splitting by {% endblock %} works perfectly.
                subparts = parts[1].split('{% endblock %}')
                
                block_content = subparts[0]
                
                content = parts[0] + '{% block content %}\n<div class="content-body">\n    <div class="container-fluid">' + block_content + '    </div>\n</div>\n{% endblock %}' + '{% endblock %}'.join(subparts[1:])
            
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
