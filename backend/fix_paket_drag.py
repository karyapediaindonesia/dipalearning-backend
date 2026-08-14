import os, re

filepath = r"c:\Users\PC-HMK\Desktop\Project\dipalearning\backend\templates\dashboard\pages\master-paket-edukasi.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML drag items
old_html_item = """                                            <div class="d-flex align-items-center">
                                                <span class="badge badge-sm badge-primary me-2">{{ lvl.course.code }}</span>
                                                <span>{{ lvl.course.name }} - {{ lvl.name }} <small class="text-muted">({{ lvl.estimated_sessions|default:0 }} Jam)</small></span>
                                            </div>
                                            <i class="fa fa-arrows-alt text-muted"></i>"""
new_html_item = """                                            <div class="d-flex align-items-center">
                                                <span class="badge badge-sm badge-primary me-2">{{ lvl.course.code }}</span>
                                                <span>{{ lvl.course.name }} - {{ lvl.name }} <small class="text-muted">({{ lvl.estimated_sessions|default:0 }} Jam)</small></span>
                                            </div>
                                            <div class="d-flex align-items-center">
                                                <button type="button" class="btn btn-xs btn-light px-2 py-1 me-2" onclick="moveItem(this)" title="Pindahkan">
                                                    <i class="fa fa-plus text-success icon-action"></i>
                                                </button>
                                                <i class="fa fa-arrows-alt text-muted handle" style="cursor: grab;" title="Tarik"></i>
                                            </div>"""
content = content.replace(old_html_item, new_html_item)

# 2. Add updateIcons and moveItem, fix SortableJS initialization, and update editPackage

new_js = """{% block master_js %}
<script src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js"></script>
<script>
    let availableSortable, selectedSortable;
    const initialLevelsHtml = $('#availableLevels').html();

    const requiredFields = [
        { id: 'pkg_name', label: 'Nama Paket' },
        { id: 'pkg_price', label: 'Harga Paket' },
        { id: 'pkg_meetings', label: 'Kuota Pertemuan' },
        { id: 'pkg_validity', label: 'Masa Berlaku' },
    ];

    function calculateTotalSessions() {
        let total = 0;
        $('#selectedLevels .drag-item').each(function() {
            total += parseInt($(this).data('sessions')) || 0;
        });
        $('#totalSessionsCount').text(total);
        
        const quota = parseInt($('#pkg_meetings').val()) || 0;
        if (total >= quota && quota > 0) {
            $('#totalSessionsCount').removeClass('badge-info badge-danger').addClass('badge-success');
        } else if (total > 0 && total < quota) {
            $('#totalSessionsCount').removeClass('badge-info badge-success').addClass('badge-danger');
        } else {
            $('#totalSessionsCount').removeClass('badge-danger badge-success').addClass('badge-info');
        }
        return total;
    }

    function showErrors(messages) {
        const list = $('#errorList');
        list.empty();
        messages.forEach(msg => list.append(`<li>${msg}</li>`));
        $('#errorBox').show();
        $('#packageModal .modal-body').scrollTop(0);
    }

    function clearErrors() {
        $('#errorBox').hide();
        $('#errorList').empty();
        requiredFields.forEach(f => $(`#${f.id}`).removeClass('is-invalid'));
    }

    function validateForm() {
        const errors = [];
        requiredFields.forEach(field => {
            const val = $(`#${field.id}`).val();
            if (!val || val.trim() === '') {
                errors.push(`<strong>${field.label}</strong> wajib diisi.`);
                $(`#${field.id}`).addClass('is-invalid');
            } else {
                $(`#${field.id}`).removeClass('is-invalid');
            }
        });

        if ($('#selectedLevels .drag-item').length === 0) {
            errors.push(`<strong>Pemetaan Level</strong> minimal satu level harus dipilih ke dalam paket.`);
        } else {
            const total = calculateTotalSessions();
            const quota = parseInt($('#pkg_meetings').val()) || 0;
            if (total < quota) {
                errors.push(`<strong>Total Jam Level (${total})</strong> tidak boleh lebih kecil dari Kuota Pertemuan Paket (${quota}).`);
            }
        }

        return errors;
    }

    function resetForm() {
        clearErrors();
        $('#packageForm')[0].reset();
        $('#pkg_id').val('');
        $('#pkg_status').val('ACTIVE');
        $('#modalTitle').text('Tambah Paket Edukasi');
        $('#btnSimpan').prop('disabled', false).html('<i class="fa fa-save me-1"></i> Simpan Data');
        
        $('#availableLevels').html(initialLevelsHtml);
        updateIcons();
        calculateTotalSessions();
        $('#selectedLevels').empty();
    }

    function updateIcons() {
        $('#availableLevels .icon-action').removeClass('fa-minus text-danger').addClass('fa-plus text-success');
        $('#selectedLevels .icon-action').removeClass('fa-plus text-success').addClass('fa-minus text-danger');
    }

    function moveItem(btn) {
        const item = $(btn).closest('.drag-item');
        const parentId = item.parent().attr('id');
        
        if (parentId === 'availableLevels') {
            item.appendTo('#selectedLevels');
        } else {
            item.appendTo('#availableLevels');
        }
        updateIcons();
        calculateTotalSessions();
    }

    function editPackage(btn) {
        const data = $(btn).data('package');
        resetForm();
        
        $('#pkg_id').val(data.id);
        $('#pkg_name').val(data.name);
        $('#pkg_price').val(data.price);
        $('#pkg_meetings').val(data.meetings_quota);
        $('#pkg_validity').val(data.validity_days);
        $('#pkg_status').val(data.status);
        
        const selectedIds = data.levels || [];
        $('#availableLevels .drag-item').each(function() {
            const itemId = $(this).data('id').toString();
            if (selectedIds.includes(itemId)) {
                $(this).appendTo('#selectedLevels');
            }
        });
        updateIcons();
        
        $('#modalTitle').text('Edit Paket Edukasi');
        $('#packageModal').modal('show');
        calculateTotalSessions();
    }

    function deletePackage(id, name) {
        hapusData(`/api/v1/academics/packages/${id}/`, name);
    }

    $(document).ready(function() {
        availableSortable = new Sortable(document.getElementById('availableLevels'), {
            group: 'shared',
            animation: 150,
            handle: '.handle',
            onEnd: function() { 
                updateIcons();
                calculateTotalSessions(); 
            }
        });

        selectedSortable = new Sortable(document.getElementById('selectedLevels'), {
            group: 'shared',
            animation: 150,
            handle: '.handle',
            onEnd: function() { 
                updateIcons();
                calculateTotalSessions(); 
            }
        });

        $('#pkg_meetings').on('input', function() { calculateTotalSessions(); });

        $('#packageForm').on('submit', function(e) {
            e.preventDefault();
            clearErrors();
            
            const clientErrors = validateForm();
            if (clientErrors.length > 0) {
                showErrors(clientErrors);
                return;
            }

            let selectedLevelIds = [];
            $('#selectedLevels .drag-item').each(function() {
                selectedLevelIds.push($(this).data('id'));
            });

            const id = $('#pkg_id').val();
            const data = {
                name: $('#pkg_name').val().trim(),
                price: parseFloat($('#pkg_price').val()),
                meetings_quota: parseInt($('#pkg_meetings').val()),
                validity_days: parseInt($('#pkg_validity').val()),
                status: $('#pkg_status').val(),
                levels: selectedLevelIds
            };

            const method = id ? 'PUT' : 'POST';
            const url = id ? `/api/v1/academics/packages/${id}/` : '/api/v1/academics/packages/';

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
                    $('#packageModal').modal('hide');
                    Swal.fire('Berhasil!', 'Data paket berhasil disimpan.', 'success').then(() => location.reload());
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

print("Updated drag-and-drop mechanics and added plus/minus buttons.")
