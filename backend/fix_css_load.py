import os
import glob

template_dir = r"c:\Users\Pipit Kiswieantoro\Desktop\Project\dipalearning\backend\templates"
html_files = glob.glob(os.path.join(template_dir, "**", "*.html"), recursive=True)

old_block = """{% for cssurl in dz_array.global.css %}
        <link rel="stylesheet" href="{% static cssurl %}">
        {% endfor %}"""
        
new_block = """{% for cssurl in dz_array.global.css %}
        {% if 'icons' in cssurl or 'vendor/animate' in cssurl or 'vendor/aos' in cssurl %}
        <link rel="stylesheet" href="{% static cssurl %}" media="print" onload="this.media='all'">
        <noscript><link rel="stylesheet" href="{% static cssurl %}"></noscript>
        {% else %}
        <link rel="stylesheet" href="{% static cssurl %}">
        {% endif %}
        {% endfor %}"""

old_block2 = """{% for cssurl in dz_array.global.css %}
    <link rel="stylesheet" href="{% static cssurl %}">
	{% endfor %}"""

new_block2 = """{% for cssurl in dz_array.global.css %}
    {% if 'icons' in cssurl or 'vendor/animate' in cssurl or 'vendor/aos' in cssurl %}
    <link rel="stylesheet" href="{% static cssurl %}" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="{% static cssurl %}"></noscript>
    {% else %}
    <link rel="stylesheet" href="{% static cssurl %}">
    {% endif %}
    {% endfor %}"""

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    if old_block in content:
        content = content.replace(old_block, new_block)
        modified = True
    if old_block2 in content:
        content = content.replace(old_block2, new_block2)
        modified = True
        
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath}")
