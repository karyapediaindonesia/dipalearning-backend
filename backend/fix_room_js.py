import os, re

filepath = r"c:\Users\PC-HMK\Desktop\Project\dipalearning\backend\templates\dashboard\pages\master-ruangan.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_js = """{% block master_js %}
<script>
    const requiredFields = [
        { id: 'branch', label: 'Cabang' },
        { id: 'code', label: 'Kode Ruangan' },
        { id: 'name', label: 'Nama Ruangan' },
        { id: 'capacity_ideal', label: 'Kapasitas Ideal' },
        { id: 'capacity_max', label: 'Kapasitas Maksimal' }
    ];

    function showErrors(messages) {
        const list = $('#errorList');
        list.empty();
        messages.forEach(msg => list.append(`<li>${msg}</li>`));
        $('#errorBox').show();
        $('#roomModal .modal-body').scrollTop(0);
    }

    function clearErrors() {
        $('#errorBox').hide();
        $('#errorList').empty();
        requiredFields.forEach(f => $(`#${f.id}`).removeClass('is-invalid'));
    }

    function validateForm() {
        const errors = [];
        requiredFields.forEach(field => {
            const val = $(`#${field.id}`).val().trim();
            if (!val) {
                errors.push(`<strong>${field.label}</strong> wajib diisi.`);
                $(`#${field.id}`).addClass('is-invalid');
            } else {
                $(`#${field.id}`).removeClass('is-invalid');
            }
        });
        return errors;
    }

    function resetForm() {
        clearErrors();
        $('#room_id').val('');
        $('#branch').val('').trigger('change');
        $('#code').val('');
        $('#name').val('');
        $('#room_type').val('CLASSROOM').trigger('change');
        $('#capacity_ideal').val('10');
        $('#capacity_max').val('15');
        $('#facilities').val('');
        $('#status').val('ACTIVE').trigger('change');
        $('#notes').val('');
        $('#modalTitle').text('Tambah Master Ruangan');
        $('#btnSimpan').prop('disabled', false).html('<i class="fa fa-save me-1"></i> Simpan Data');
    }

    function editRoom(btn) {
        const $btn = $(btn);
        resetForm();
        $('#room_id').val($btn.data('id'));
        $('#branch').val($btn.data('branch')).trigger('change');
        $('#code').val($btn.data('code'));
        $('#name').val($btn.data('name'));
        $('#room_type').val($btn.data('type')).trigger('change');
        $('#capacity_ideal').val($btn.data('ideal'));
        $('#capacity_max').val($btn.data('max'));
        $('#facilities').val($btn.data('facilities'));
        $('#status').val($btn.data('status')).trigger('change');
        $('#notes').val($btn.data('notes'));
        $('#modalTitle').text('Edit Master Ruangan');
        $('#roomModal').modal('show');
    }

    function viewRoom(btn) {
        const $btn = $(btn);
        
        let statusBadge = '<span class="badge light badge-success">Aktif</span>';
        if($btn.data('status') === 'INACTIVE') statusBadge = '<span class="badge light badge-warning">Nonaktif</span>';
        else if($btn.data('status') === 'MAINTENANCE') statusBadge = '<span class="badge light badge-danger">Maintenance</span>';
        
        let html = `
            <table class="table table-borderless table-sm">
                <tr><td width="30%" class="text-muted">Cabang</td><td width="5%">:</td><td><strong>${$btn.data('branch-name')}</strong></td></tr>
                <tr><td class="text-muted">Kode Ruangan</td><td>:</td><td><strong>${$btn.data('code')}</strong></td></tr>
                <tr><td class="text-muted">Nama Ruangan</td><td>:</td><td><strong>${$btn.data('name')}</strong></td></tr>
                <tr><td class="text-muted">Jenis Ruangan</td><td>:</td><td>${$btn.data('type')}</td></tr>
                <tr><td class="text-muted">Kapasitas (Ideal/Max)</td><td>:</td><td>${$btn.data('ideal')} / ${$btn.data('max')}</td></tr>
                <tr><td class="text-muted">Fasilitas</td><td>:</td><td>${$btn.data('facilities') || '-'}</td></tr>
                <tr><td class="text-muted">Status</td><td>:</td><td>${statusBadge}</td></tr>
            </table>
            <div class="mt-3">
                <h6 class="text-primary mb-2"><i class="la la-sticky-note me-2"></i> Catatan</h6>
                <div class="p-3 bg-light rounded">${$btn.data('notes') || '-'}</div>
            </div>
        `;
        $('#viewModalContent').html(html);
        $('#viewRoomModal').modal('show');
    }

    function deleteRoom(id, name) {
        hapusData(`/api/v1/branches/rooms/${id}/`, name);
    }

    $(document).ready(function() {
        if ($.fn.DataTable.isDataTable('#roomTable')) {
            $('#roomTable').DataTable().destroy();
        }
        $('#roomTable').DataTable({
            language: {
                paginate: {
                  next: '<i class="fa fa-angle-double-right" aria-hidden="true"></i>',
                  previous: '<i class="fa fa-angle-double-left" aria-hidden="true"></i>' 
                }
            }
        });

        $('#roomForm').on('submit', function(e) {
            e.preventDefault();
            clearErrors();
            const clientErrors = validateForm();
            if (clientErrors.length > 0) {
                showErrors(clientErrors);
                return;
            }

            const id = $('#room_id').val();
            let facilities = $('#facilities').val().split(',').map(s => s.trim()).filter(s => s);
            
            const data = {
                branch: $('#branch').val(),
                code: $('#code').val().trim(),
                name: $('#name').val().trim(),
                room_type: $('#room_type').val(),
                capacity_ideal: parseInt($('#capacity_ideal').val()),
                capacity_max: parseInt($('#capacity_max').val()),
                facilities: facilities,
                status: $('#status').val(),
                notes: $('#notes').val().trim(),
            };

            const method = id ? 'PUT' : 'POST';
            const url = id ? `/api/v1/branches/rooms/${id}/` : '/api/v1/branches/rooms/';

            $('#btnSimpan').prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-1"></span> Menyimpan...');

            fetch(url, {
                method: method,
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify(data)
            })
            .then(async response => {
                const json = await response.json().catch(() => null);
                if (response.ok) {
                    location.reload();
                } else {
                    const serverErrors = [];
                    if (json && json.error && json.error.details) {
                        for (const [field, msgs] of Object.entries(json.error.details)) {
                            serverErrors.push(`<strong>${field}:</strong> ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`);
                        }
                    } else if (json && typeof json === 'object') {
                        for (const [field, msgs] of Object.entries(json)) {
                            serverErrors.push(`<strong>${field}:</strong> ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`);
                        }
                    } else {
                        serverErrors.push(`Error: ${response.status}`);
                    }
                    showErrors(serverErrors);
                    $('#btnSimpan').prop('disabled', false).html('<i class="fa fa-save me-1"></i> Simpan Data');
                }
            })
            .catch(err => {
                showErrors([`Gagal terhubung ke server: <strong>${err.message}</strong>.`]);
                $('#btnSimpan').prop('disabled', false).html('<i class="fa fa-save me-1"></i> Simpan Data');
            });
        });
    });
</script>
{% endblock %}"""

content = re.sub(r'\{%\s*block master_js\s*%\}.*?\{%\s*endblock\s*%\}', new_js, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("JS Restored successfully.")
