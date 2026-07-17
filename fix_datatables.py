import os
import re

css_to_add = """
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
"""

dt_config = """{
            language: {
                search:       "Cari:",
                lengthMenu:   "Tampilkan _MENU_ data",
                info:         "Menampilkan _START_-_END_ dari _TOTAL_ data",
                zeroRecords:  "Tidak ada data ditemukan.",
                emptyTable:   "Tidak ada data. Klik tombol Tambah.",
                paginate: {
                    previous: '<i class="fa fa-angle-double-left"></i>',
                    next:     '<i class="fa fa-angle-double-right"></i>'
                }
            }
        }"""

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
        
        # 1. Add CSS if missing
        if '.dataTables_wrapper .dataTables_paginate' not in content:
            # Insert after {% block additional_css %}
            content = content.replace('{% block additional_css %}', '{% block additional_css %}' + css_to_add)

        # 2. Add language to DataTable
        if '.DataTable();' in content:
            content = content.replace('.DataTable();', f'.DataTable({dt_config});')
            
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
