import os

base_dir = r'c:\dipalearning\backend\templates\dashboard\pages'

ruangan_html = """{% extends 'dashboard/base.html' %}
{% load static %}

{% block title %}Master Ruangan | DIPA Learning{% endblock %}

{% block content %}
<div class="row page-titles">
    <ol class="breadcrumb">
        <li class="breadcrumb-item active"><a href="javascript:void(0)">Data Master</a></li>
        <li class="breadcrumb-item"><a href="javascript:void(0)">Master Ruangan</a></li>
    </ol>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h4 class="card-title">Data Master Ruangan</h4>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#roomModal" onclick="resetForm()">
                    <i class="fa fa-plus me-2"></i>Tambah Ruangan
                </button>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table id="roomTable" class="display" style="min-width: 845px">
                        <thead>
                            <tr>
                                <th>Cabang</th>
                                <th>Kode</th>
                                <th>Nama Ruangan</th>
                                <th>Jenis</th>
                                <th>Kapasitas</th>
                                <th>Status</th>
                                <th>Aksi</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for room in rooms %}
                            <tr>
                                <td>{{ room.branch.name }}</td>
                                <td><strong>{{ room.code }}</strong></td>
                                <td>{{ room.name }}</td>
                                <td>{{ room.get_room_type_display }}</td>
                                <td>{{ room.capacity_ideal }} / {{ room.capacity_max }}</td>
                                <td>
                                    {% if room.status == 'ACTIVE' %}
                                    <span class="badge light badge-success">Aktif</span>
                                    {% elif room.status == 'INACTIVE' %}
                                    <span class="badge light badge-warning">Nonaktif</span>
                                    {% else %}
                                    <span class="badge light badge-danger">Maintenance</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <div class="d-flex">
                                        <button class="btn btn-primary shadow btn-xs sharp me-1" 
                                                data-room='{"id":"{{ room.id }}", "branch":"{{ room.branch_id }}", "code":"{{ room.code|escapejs }}", "name":"{{ room.name|escapejs }}", "room_type":"{{ room.room_type }}", "capacity_ideal":"{{ room.capacity_ideal }}", "capacity_max":"{{ room.capacity_max }}", "facilities":{{ room.facilities|safe|default:"[]" }}, "status":"{{ room.status }}", "notes":"{{ room.notes|escapejs }}"}'
                                                onclick="editRoom(this)" title="Edit">
                                            <i class="fas fa-pencil-alt"></i>
                                        </button>
                                        <button class="btn btn-danger shadow btn-xs sharp" onclick="deleteRoom({{ room.id }}, '{{ room.name|escapejs }}')" title="Hapus">
                                            <i class="fa fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal Form -->
<div class="modal fade" id="roomModal">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="modalTitle">Tambah Master Ruangan</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div id="errorBox" class="alert alert-danger" style="display: none;">
                    <ul id="errorList" class="mb-0"></ul>
                </div>
                <form id="roomForm">
                    <input type="hidden" id="room_id">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Cabang <span class="text-danger">*</span></label>
                            <select class="form-control" id="branch">
                                <option value="">Pilih Cabang</option>
                                {% for branch in branches %}
                                <option value="{{ branch.id }}">{{ branch.code }} - {{ branch.name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Kode Ruangan <span class="text-danger">*</span></label>
                            <input type="text" class="form-control" id="code" placeholder="Contoh: R-01">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Nama Ruangan <span class="text-danger">*</span></label>
                            <input type="text" class="form-control" id="name" placeholder="Contoh: Kelas Alpha">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Jenis Ruangan <span class="text-danger">*</span></label>
                            <select class="form-control" id="room_type">
                                <option value="CLASSROOM">Ruang Kelas</option>
                                <option value="PRIVATE">Ruang Privat</option>
                                <option value="GROUP">Ruang Kelompok</option>
                                <option value="LABORATORY">Laboratorium</option>
                                <option value="MEETING">Ruang Rapat</option>
                                <option value="HALL">Aula/Multifungsi</option>
                                <option value="ADMINISTRATION">Ruang Administrasi</option>
                                <option value="OTHER">Lainnya</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Kapasitas Ideal <span class="text-danger">*</span></label>
                            <input type="number" class="form-control" id="capacity_ideal" value="10">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Kapasitas Maksimal <span class="text-danger">*</span></label>
                            <input type="number" class="form-control" id="capacity_max" value="15">
                        </div>
                        <div class="col-md-12 mb-3">
                            <label class="form-label">Fasilitas Ruangan</label>
                            <input type="text" class="form-control" id="facilities" placeholder="Pisahkan dengan koma. Contoh: AC, Proyektor">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Status Ruangan <span class="text-danger">*</span></label>
                            <select class="form-control" id="status">
                                <option value="ACTIVE" selected>Aktif</option>
                                <option value="INACTIVE">Nonaktif</option>
                                <option value="MAINTENANCE">Maintenance</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Catatan</label>
                            <textarea class="form-control" id="notes" rows="2"></textarea>
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer d-flex justify-content-between align-items-center">
                <small class="text-muted"><span class="text-danger">*</span> = wajib diisi</small>
                <div>
                    <button type="button" class="btn btn-danger light me-2" data-bs-dismiss="modal">Batal</button>
                    <button type="button" class="btn btn-primary" id="btnSimpan" onclick="saveRoom()">
                        <i class="fa fa-save me-1"></i> Simpan Data
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block additional_js %}
<script src="{% static 'dashboard/vendor/datatables/js/jquery.dataTables.min.js' %}"></script>
<script>
    .ready(function() { #roomTable.DataTable(); });
    function showErrors(msgs) { #errorList.html(msgs.map(m => <li></li>).join('')); #errorBox.show(); }
    function resetForm() {
        #errorBox.hide(); #room_id.val(''); #branch.val(''); #code.val(''); #name.val('');
        #room_type.val('CLASSROOM'); #capacity_ideal.val('10'); #capacity_max.val('15');
        #facilities.val(''); #status.val('ACTIVE'); #notes.val(''); #modalTitle.text('Tambah Ruangan');
    }
    function editRoom(btn) {
        const d = .data('room'); resetForm();
        #room_id.val(d.id); #branch.val(d.branch); #code.val(d.code); #name.val(d.name);
        #room_type.val(d.room_type); #capacity_ideal.val(d.capacity_ideal); #capacity_max.val(d.capacity_max);
        #facilities.val((d.facilities || []).join(', ')); #status.val(d.status); #notes.val(d.notes);
        #modalTitle.text('Edit Ruangan'); #roomModal.modal('show');
    }
    function saveRoom() {
        const id = #room_id.val();
        const data = {
            branch: #branch.val(), code: #code.val(), name: #name.val(),
            room_type: #room_type.val(), capacity_ideal: parseInt(#capacity_ideal.val()),
            capacity_max: parseInt(#capacity_max.val()),
            facilities: #facilities.val().split(',').map(s=>s.trim()).filter(s=>s),
            status: #status.val(), notes: #notes.val()
        };
        const method = id ? 'PUT' : 'POST'; const url = id ? /api/v1/branches/rooms// : '/api/v1/branches/rooms/';
        fetch(url, { method: method, headers: {'Content-Type': 'application/json', 'X-CSRFToken': '{{ csrf_token }}'}, body: JSON.stringify(data) })
        .then(r => r.ok ? location.reload() : r.json().then(j => showErrors([JSON.stringify(j)])));
    }
    function deleteRoom(id, name) {
        if(confirm(Hapus ?)) {
            fetch(/api/v1/branches/rooms//, { method: 'DELETE', headers: {'X-CSRFToken': '{{ csrf_token }}'} })
            .then(r => r.ok ? location.reload() : alert('Gagal'));
        }
    }
</script>
{% endblock %}
"""

kursus_html = """{% extends 'dashboard/base.html' %}
{% load static %}
{% block title %}Master Kursus | DIPA Learning{% endblock %}
{% block content %}
<div class="row page-titles">
    <ol class="breadcrumb">
        <li class="breadcrumb-item active"><a href="javascript:void(0)">Data Master</a></li>
        <li class="breadcrumb-item"><a href="javascript:void(0)">Master Kursus</a></li>
    </ol>
</div>
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h4 class="card-title">Data Master Kursus</h4>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#courseModal" onclick="resetForm()">
                    <i class="fa fa-plus me-2"></i>Tambah Kursus
                </button>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table id="courseTable" class="display" style="min-width: 845px">
                        <thead>
                            <tr>
                                <th>Kode</th><th>Nama Kursus</th><th>Kategori</th><th>Mode</th><th>Durasi</th><th>Status</th><th>Aksi</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for course in courses %}
                            <tr>
                                <td><strong>{{ course.code }}</strong></td><td>{{ course.name }}</td>
                                <td>{{ course.get_category_display }}</td><td>{{ course.get_learning_mode_display }}</td>
                                <td>{{ course.default_duration }} mnt</td>
                                <td>{% if course.status == 'ACTIVE' %}<span class="badge light badge-success">Aktif</span>{% else %}<span class="badge light badge-warning">Nonaktif</span>{% endif %}</td>
                                <td>
                                    <div class="d-flex">
                                        <button class="btn btn-primary shadow btn-xs sharp me-1" 
                                                data-obj='{"id":"{{ course.id }}", "code":"{{ course.code|escapejs }}", "name":"{{ course.name|escapejs }}", "category":"{{ course.category }}", "learning_type":"{{ course.learning_type }}", "learning_mode":"{{ course.learning_mode }}", "default_duration":"{{ course.default_duration }}", "status":"{{ course.status }}", "notes":"{{ course.notes|escapejs }}"}'
                                                onclick="editCourse(this)" title="Edit">
                                            <i class="fas fa-pencil-alt"></i>
                                        </button>
                                        <button class="btn btn-danger shadow btn-xs sharp" onclick="deleteCourse({{ course.id }}, '{{ course.name|escapejs }}')" title="Hapus">
                                            <i class="fa fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="courseModal">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="modalTitle">Tambah Master Kursus</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div id="errorBox" class="alert alert-danger" style="display: none;"><ul id="errorList" class="mb-0"></ul></div>
                <form id="courseForm">
                    <input type="hidden" id="course_id">
                    <div class="row">
                        <div class="col-md-6 mb-3"><label class="form-label">Kode Kursus *</label><input type="text" class="form-control" id="code"></div>
                        <div class="col-md-6 mb-3"><label class="form-label">Nama Kursus *</label><input type="text" class="form-control" id="name"></div>
                        <div class="col-md-6 mb-3"><label class="form-label">Kategori *</label>
                            <select class="form-control" id="category">
                                <option value="ACADEMIC">Akademik</option><option value="LANGUAGE">Bahasa</option>
                                <option value="TECHNOLOGY">Teknologi</option><option value="CREATIVITY">Kreativitas</option>
                                <option value="PRESCHOOL">Persiapan sekolah</option><option value="SELF_DEV">Pengembangan diri</option><option value="SPECIAL">Program khusus</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3"><label class="form-label">Tipe Belajar *</label>
                            <select class="form-control" id="learning_type"><option value="INDIVIDUAL">Individual</option><option value="GROUP">Kelompok</option><option value="BOTH">Keduanya</option></select>
                        </div>
                        <div class="col-md-6 mb-3"><label class="form-label">Mode Belajar *</label>
                            <select class="form-control" id="learning_mode"><option value="OFFLINE">Tatap muka</option><option value="ONLINE">Online</option><option value="HYBRID">Hybrid</option></select>
                        </div>
                        <div class="col-md-6 mb-3"><label class="form-label">Durasi (menit) *</label><input type="number" class="form-control" id="default_duration" value="60"></div>
                        <div class="col-md-6 mb-3"><label class="form-label">Status *</label><select class="form-control" id="status"><option value="ACTIVE">Aktif</option><option value="INACTIVE">Nonaktif</option></select></div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Batal</button>
                <button type="button" class="btn btn-primary" onclick="saveCourse()">Simpan</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}
{% block additional_js %}
<script src="{% static 'dashboard/vendor/datatables/js/jquery.dataTables.min.js' %}"></script>
<script>
    .ready(function() { #courseTable.DataTable(); });
    function showErrors(msgs) { #errorList.html(msgs.map(m => <li></li>).join('')); #errorBox.show(); }
    function resetForm() { #errorBox.hide(); #course_id.val(''); #code.val(''); #name.val(''); #modalTitle.text('Tambah Kursus'); }
    function editCourse(btn) {
        const d = .data('obj'); resetForm();
        #course_id.val(d.id); #code.val(d.code); #name.val(d.name); #category.val(d.category);
        #learning_type.val(d.learning_type); #learning_mode.val(d.learning_mode); #default_duration.val(d.default_duration);
        #status.val(d.status); #modalTitle.text('Edit Kursus'); #courseModal.modal('show');
    }
    function saveCourse() {
        const id = #course_id.val();
        const data = { code: #code.val(), name: #name.val(), category: #category.val(), learning_type: #learning_type.val(), learning_mode: #learning_mode.val(), default_duration: parseInt(#default_duration.val()), status: #status.val() };
        const method = id ? 'PUT' : 'POST'; const url = id ? /api/v1/academics/courses// : '/api/v1/academics/courses/';
        fetch(url, { method: method, headers: {'Content-Type': 'application/json', 'X-CSRFToken': '{{ csrf_token }}'}, body: JSON.stringify(data) }).then(r => r.ok ? location.reload() : r.json().then(j => showErrors([JSON.stringify(j)])));
    }
    function deleteCourse(id, name) { if(confirm(Hapus ?)) fetch(/api/v1/academics/courses//, {method: 'DELETE', headers: {'X-CSRFToken': '{{ csrf_token }}'}}).then(r => r.ok ? location.reload() : alert('Gagal')); }
</script>
{% endblock %}
"""

level_html = """{% extends 'dashboard/base.html' %}
{% load static %}
{% block title %}Master Level | DIPA Learning{% endblock %}
{% block content %}
<div class="row page-titles">
    <ol class="breadcrumb">
        <li class="breadcrumb-item active"><a href="javascript:void(0)">Data Master</a></li>
        <li class="breadcrumb-item"><a href="javascript:void(0)">Master Level</a></li>
    </ol>
</div>
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h4 class="card-title">Data Master Level</h4>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#levelModal" onclick="resetForm()">
                    <i class="fa fa-plus me-2"></i>Tambah Level
                </button>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table id="levelTable" class="display" style="min-width: 845px">
                        <thead>
                            <tr>
                                <th>Kursus</th><th>Kode</th><th>Nama Level</th><th>Urutan</th><th>Status</th><th>Aksi</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for level in levels %}
                            <tr>
                                <td>{{ level.course.name }}</td><td><strong>{{ level.code }}</strong></td><td>{{ level.name }}</td><td>{{ level.order }}</td>
                                <td>{% if level.status == 'ACTIVE' %}<span class="badge light badge-success">Aktif</span>{% else %}<span class="badge light badge-warning">Nonaktif</span>{% endif %}</td>
                                <td>
                                    <div class="d-flex">
                                        <button class="btn btn-primary shadow btn-xs sharp me-1" 
                                                data-obj='{"id":"{{ level.id }}", "course":"{{ level.course_id }}", "code":"{{ level.code|escapejs }}", "name":"{{ level.name|escapejs }}", "order":"{{ level.order }}", "prerequisite":"{{ level.prerequisite_id|default:"" }}", "use_course_duration":{{ level.use_course_duration|yesno:"true,false" }}, "custom_duration":"{{ level.custom_duration|default:"" }}", "estimated_sessions":"{{ level.estimated_sessions }}", "status":"{{ level.status }}"}'
                                                onclick="editLevel(this)" title="Edit">
                                            <i class="fas fa-pencil-alt"></i>
                                        </button>
                                        <button class="btn btn-danger shadow btn-xs sharp" onclick="deleteLevel({{ level.id }}, '{{ level.name|escapejs }}')" title="Hapus">
                                            <i class="fa fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
<div class="modal fade" id="levelModal">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="modalTitle">Tambah Master Level</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div id="errorBox" class="alert alert-danger" style="display: none;"><ul id="errorList" class="mb-0"></ul></div>
                <form id="levelForm">
                    <input type="hidden" id="level_id">
                    <div class="row">
                        <div class="col-md-6 mb-3"><label class="form-label">Kursus *</label>
                            <select class="form-control" id="course"><option value="">Pilih Kursus</option>{% for course in courses %}<option value="{{ course.id }}">{{ course.name }}</option>{% endfor %}</select>
                        </div>
                        <div class="col-md-6 mb-3"><label class="form-label">Kode Level *</label><input type="text" class="form-control" id="code"></div>
                        <div class="col-md-6 mb-3"><label class="form-label">Nama Level *</label><input type="text" class="form-control" id="name"></div>
                        <div class="col-md-6 mb-3"><label class="form-label">Urutan *</label><input type="number" class="form-control" id="order" value="1"></div>
                        <div class="col-md-6 mb-3"><label class="form-label">Gunakan Durasi Kursus</label><select class="form-control" id="use_course_duration"><option value="true">Ya</option><option value="false">Tidak (Custom)</option></select></div>
                        <div class="col-md-6 mb-3"><label class="form-label">Durasi Khusus (menit)</label><input type="number" class="form-control" id="custom_duration"></div>
                        <div class="col-md-6 mb-3"><label class="form-label">Estimasi Pertemuan *</label><input type="number" class="form-control" id="estimated_sessions" value="10"></div>
                        <div class="col-md-6 mb-3"><label class="form-label">Status *</label><select class="form-control" id="status"><option value="ACTIVE">Aktif</option><option value="INACTIVE">Nonaktif</option></select></div>
                    </div>
                </form>
            </div>
            <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Batal</button><button type="button" class="btn btn-primary" onclick="saveLevel()">Simpan</button></div>
        </div>
    </div>
</div>
{% endblock %}
{% block additional_js %}
<script src="{% static 'dashboard/vendor/datatables/js/jquery.dataTables.min.js' %}"></script>
<script>
    .ready(function() { #levelTable.DataTable(); });
    function showErrors(msgs) { #errorList.html(msgs.map(m => <li></li>).join('')); #errorBox.show(); }
    function resetForm() { #errorBox.hide(); #level_id.val(''); #course.val(''); #code.val(''); #name.val(''); #modalTitle.text('Tambah Level'); }
    function editLevel(btn) {
        const d = .data('obj'); resetForm();
        #level_id.val(d.id); #course.val(d.course); #code.val(d.code); #name.val(d.name); #order.val(d.order);
        #use_course_duration.val(d.use_course_duration ? 'true' : 'false'); #custom_duration.val(d.custom_duration);
        #estimated_sessions.val(d.estimated_sessions); #status.val(d.status); #modalTitle.text('Edit Level'); #levelModal.modal('show');
    }
    function saveLevel() {
        const id = #level_id.val();
        const data = { course: #course.val(), code: #code.val(), name: #name.val(), order: parseInt(#order.val()), use_course_duration: #use_course_duration.val() === 'true', custom_duration: #custom_duration.val() ? parseInt(#custom_duration.val()) : null, estimated_sessions: parseInt(#estimated_sessions.val()), status: #status.val() };
        const method = id ? 'PUT' : 'POST'; const url = id ? /api/v1/academics/levels// : '/api/v1/academics/levels/';
        fetch(url, { method: method, headers: {'Content-Type': 'application/json', 'X-CSRFToken': '{{ csrf_token }}'}, body: JSON.stringify(data) }).then(r => r.ok ? location.reload() : r.json().then(j => showErrors([JSON.stringify(j)])));
    }
    function deleteLevel(id, name) { if(confirm(Hapus ?)) fetch(/api/v1/academics/levels//, {method: 'DELETE', headers: {'X-CSRFToken': '{{ csrf_token }}'}}).then(r => r.ok ? location.reload() : alert('Gagal')); }
</script>
{% endblock %}
"""

with open(os.path.join(base_dir, 'master-ruangan.html'), 'w', encoding='utf-8') as f:
    f.write(ruangan_html)
with open(os.path.join(base_dir, 'master-kursus.html'), 'w', encoding='utf-8') as f:
    f.write(kursus_html)
with open(os.path.join(base_dir, 'master-level.html'), 'w', encoding='utf-8') as f:
    f.write(level_html)

print("Templates generated successfully.")
