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
        print(f'{f} has additional_css: {"{% block additional_css %}" in content}')
        print(f'{f} has CSS: {".dataTables_wrapper .dataTables_paginate" in content}')
