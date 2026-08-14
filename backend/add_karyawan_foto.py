import re

filepath = r'c:\Users\PC-HMK\Desktop\Project\dipalearning\backend\templates\dashboard\pages\master-karyawan.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add View Button
view_btn = '''                                                <button class="btn btn-info shadow btn-xs sharp me-1" 
                                                        onclick="viewEmployee('{{ emp.id }}')" title="Lihat Detail">
                                                    <i class="fas fa-eye"></i>
                                                </button>
                                                <button class="btn btn-primary shadow btn-xs sharp me-1"'''
content = content.replace(
    '<button class="btn btn-primary shadow btn-xs sharp me-1"', 
    view_btn,
    1
)

# 2. Add Photo Input in Form (below Gender)
photo_input = '''                        <div class="col-md-3 mb-3">
                            <label class="form-label">Jenis Kelamin</label>
                            <select class="form-control" id="gender">
                                <option value="">-- Pilih --</option>
                                <option value="L">Laki-laki</option>
                                <option value="P">Perempuan</option>
                            </select>
                        </div>
                        <div class="col-md-12 mb-3">
                            <label class="form-label">Foto Karyawan</label>
                            <input type="file" class="form-control" id="photo" accept="image/*">
                            <small class="text-muted">Biarkan kosong jika tidak ingin mengubah foto.</small>
                        </div>'''
content = content.replace(
    '''                        <div class="col-md-3 mb-3">
                            <label class="form-label">Jenis Kelamin</label>
                            <select class="form-control" id="gender">
                                <option value="">-- Pilih --</option>
                                <option value="L">Laki-laki</option>
                                <option value="P">Perempuan</option>
                            </select>
                        </div>''', 
    photo_input,
    1
)

# 3. Add View Modal before endblock (line 218 normally)
view_modal = '''<!-- Modal Detail Karyawan -->
<div class="modal fade" id="viewEmployeeModal" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Detail Karyawan: <span id="view_full_name_title" class="text-primary"></span></h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="text-center mb-4">
                    <img id="view_photo" src="" class="rounded-circle img-thumbnail" width="120" height="120" style="object-fit: cover; display: none;">
                </div>
                <table class="table table-borderless table-sm">
                    <tr><td width="30%" class="text-muted">Nama Lengkap</td><td width="5%">:</td><td><strong id="view_full_name"></strong></td></tr>
                    <tr><td class="text-muted">Nama Panggilan</td><td>:</td><td id="view_nickname"></td></tr>
                    <tr><td class="text-muted">Jenis Kelamin</td><td>:</td><td id="view_gender"></td></tr>
                    <tr><td class="text-muted">Tempat/Tanggal Lahir</td><td>:</td><td id="view_birth"></td></tr>
                    <tr><td class="text-muted">NIK (KTP)</td><td>:</td><td id="view_nik"></td></tr>
                    <tr><td class="text-muted">NPWP</td><td>:</td><td id="view_npwp"></td></tr>
                    <tr><td class="text-muted">Telepon / WA</td><td>:</td><td id="view_contacts"></td></tr>
                    <tr><td class="text-muted">Email (Pribadi / Kerja)</td><td>:</td><td id="view_emails"></td></tr>
                    <tr><td class="text-muted">Alamat</td><td>:</td><td id="view_address"></td></tr>
                    <tr><td class="text-muted">Tipe Karyawan</td><td>:</td><td id="view_type"></td></tr>
                    <tr><td class="text-muted">Jabatan / Departemen</td><td>:</td><td id="view_job"></td></tr>
                    <tr><td class="text-muted">Tanggal Bergabung</td><td>:</td><td id="view_join"></td></tr>
                    <tr><td class="text-muted">Status</td><td>:</td><td id="view_status"></td></tr>
                </table>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Tutup</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

content = content.replace('{% endblock %}', view_modal, 1)

# 4. Modify form submission success to handle photo upload
# Find: success: function() {
#           Swal.fire('Berhasil!', 'Data berhasil disimpan.', 'success').then(() => location.reload());
#       },
# Replace it with the photo patch request

upload_logic = '''success: function(resp) {
                const empId = id ? id : (resp.data ? resp.data.id : resp.id);
                const photoInput = $('#photo')[0];
                if (photoInput && photoInput.files.length > 0) {
                    const fd = new FormData();
                    fd.append('photo', photoInput.files[0]);
                    
                    $.ajax({
                        url: `/api/v1/hr/employees/${empId}/`,
                        type: 'PATCH',
                        data: fd,
                        processData: false,
                        contentType: false,
                        headers: {'X-CSRFToken': '{{ csrf_token }}'},
                        success: function() {
                            Swal.fire('Berhasil!', 'Data dan foto berhasil disimpan.', 'success').then(() => location.reload());
                        },
                        error: function(xhr) {
                            alert('Data tersimpan, tapi foto gagal diunggah: ' + xhr.responseText);
                            location.reload();
                        }
                    });
                } else {
                    Swal.fire('Berhasil!', 'Data berhasil disimpan.', 'success').then(() => location.reload());
                }
            },'''

content = content.replace('''success: function() {
                Swal.fire('Berhasil!', 'Data berhasil disimpan.', 'success').then(() => location.reload());
            },''', upload_logic)


# 5. Add viewEmployee(id) JS function
# We will inject it right after deleteEmployee function
view_js = '''    function viewEmployee(id) {
        $.get(`/api/v1/hr/employees/${id}/`, function(response) {
            const data = response.data || response;
            $('#view_full_name_title').text(data.full_name);
            $('#view_full_name').text(data.full_name);
            $('#view_nickname').text(data.nickname || '-');
            $('#view_gender').text(data.gender === 'L' ? 'Laki-laki' : (data.gender === 'P' ? 'Perempuan' : '-'));
            $('#view_birth').text((data.birth_place || '-') + ' / ' + (data.birth_date || '-'));
            $('#view_nik').text(data.nik || '-');
            $('#view_npwp').text(data.npwp || '-');
            $('#view_contacts').text((data.phone || '-') + ' / ' + (data.whatsapp || '-'));
            $('#view_emails').text((data.personal_email || '-') + ' / ' + (data.work_email || '-'));
            $('#view_address').text(data.address || '-');
            $('#view_type').text(data.employee_type || '-');
            
            // Wait, we just get job_position ID from the API. We can use selected text from the dropdown if we want,
            // or we just show the ID if it's too much work. Since we only have the ID, let's look it up in the dropdown:
            const jobText = $('#job_position option[value="'+data.job_position+'"]').text() || data.job_position;
            
            $('#view_job').text(jobText + ' / ' + (data.department || '-'));
            $('#view_join').text(data.join_date || '-');
            
            let statusBadge = '<span class="badge light badge-success">Aktif</span>';
            if(data.status === 'INACTIVE') statusBadge = '<span class="badge light badge-danger">Nonaktif</span>';
            $('#view_status').html(statusBadge);

            if (data.photo) {
                $('#view_photo').attr('src', data.photo).show();
            } else {
                $('#view_photo').hide().attr('src', '');
            }
            
            $('#viewEmployeeModal').modal('show');
        });
    }

    function deleteEmployee(id, name) {'''

content = content.replace('    function deleteEmployee(id, name) {', view_js)

# Clear photo on add/edit
content = content.replace("        $('#nickname').val('');", "        $('#nickname').val('');\n        $('#photo').val('');")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Modifications done.")
