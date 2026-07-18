# Arsitektur Sistem & Alur Aplikasi Dipa Learning

Dokumen ini berfungsi sebagai peta cetak biru (*blueprint*) dari keseluruhan arsitektur, alur data, dan standar penulisan kode untuk aplikasi **Dipa Learning**. Dokumen ini wajib dibaca dan dipatuhi setiap kali terjadi penambahan fitur baru atau perbaikan *bug*, agar sistem tetap kokoh dan berjalan sesuai standar internasional.

---

## 1. Topologi Modul (Django Apps)
Aplikasi ini dikembangkan menggunakan arsitektur monolitik modular (*modular monolith*) Django. Modul-modul (*apps*) dibagi berdasarkan ranah bisnis masing-masing:
- **`dashboard`**: Mengatur seluruh antarmuka pengguna (UI/UX) web, manajemen *template*, dan *routing* halaman frontend.
- **`accounts`**: Modul manajemen otentikasi (User, Profil, Registrasi).
- **`core`**: Menyimpan konfigurasi data krusial yang bersifat global (seperti Data Provinsi, Kota/Kabupaten, dsb).
- **`academics`**: Menangani data pengajaran (Kursus, Kelas, Tahun Ajaran, Level/Jenjang, dsb).
- **`students`**: Manajemen siklus hidup siswa (Prospek, Registrasi, *Enrollment*, hingga Kelulusan).
- **`finance` & `billing`**: Modul siklus keuangan, tagihan (*invoice*), metode bayar, dan manajemen kategori biaya.
- **`hr` & `attendance`**: Menangani pengelolaan SDM, master karyawan, jabatan, dan absensi (termasuk alasan absen/hari libur).
- **`branches`**: Modul pengelolaan cabang (Kantor Pusat, Cabang, Unit).
- **`audit`**: Pencatatan jejak (audit trail) untuk aksi-aksi kritikal dalam sistem.

---

## 2. Standarisasi Frontend & Antarmuka (UI/UX)
Kita telah menerapkan prinsip pengembangan web yang efisien (*DRY - Don't Repeat Yourself*).

### A. Template Inheritance (Pewarisan Template)
Setiap halaman daftar master data **Wajib** mewarisi (extend) *Base Template* global:
```django
{% extends 'dashboard/elements/layouts/master_list_base.html' %}
```
**Fasilitas bawaan dari `master_list_base.html`:**
1. Kerangka tata letak *Card* putih standar yang responsif.
2. Navigasi *Breadcrumbs*.
3. Inisialisasi otomatis untuk pustaka-pustaka utama:
   - **DataTables**: Setiap tabel dengan class `display` akan otomatis memiliki fitur *Search*, *Pagination*, dan *Sorting* tanpa perlu menulis JS lagi.
   - **SweetAlert2**: Pustaka kotak dialog/notifikasi.
   - **Select2**: Pustaka interaktif untuk *dropdown* pencarian.

### B. Standardisasi Autentikasi Frontend (Login Flow)
- Alur *login* dan *logout* diatur secara terpusat di `backend/config/settings/base.py` (`LOGIN_REDIRECT_URL` & `LOGOUT_REDIRECT_URL`).
- Setiap halaman terproteksi menggunakan parameter `?next=`. Jika pengguna yang belum login mencoba mengakses `/master-level/`, mereka akan diarahkan ke login, dan setelah login sukses, form login wajib memiliki input hidden `next` yang mengarahkan mereka secara otomatis kembali ke `/master-level/`.
- Halaman *views* wajib diproteksi menggunakan *decorator* `@login_required` dan bukan dengan pengecekan manual if-else.

---

## 3. Alur Komunikasi Data (CRUD & API)

### A. Komunikasi AJAX (Fetch/jQuery)
Antarmuka Web (*dashboard*) berkomunikasi dengan *Backend* melalui antarmuka REST API bawaan.
- Seluruh permintaan POST/PUT/DELETE wajib melampirkan `X-CSRFToken` di dalam parameter *Headers*.
- Operasi penarikan data dinamis (misalnya saat memilih "Provinsi", maka *dropdown* "Kota" otomatis terisi) dilakukan secara *asynchronous* (Fetch API / AJAX) tanpa *reload* halaman.

### B. Prosedur Hapus (Delete Flow) Terstandarisasi
Tindakan `DELETE` adalah aksi yang amat kritikal. Oleh karena itu, modul hapus diatur secara global di dalam `backend/static/dashboard/js/crud-helper.js`.
**Aturan Hapus:**
1. Aksi penghapusan dilarang memanggil *API Delete* secara langsung.
2. Aksi penghapusan harus memanggil fungsi terpusat `hapusData(url_endpoint, nama_item)`.
3. `hapusData` akan selalu memunculkan konfirmasi peringatan `SweetAlert` (berstandar UX internasional) terlebih dahulu. Hanya jika *user* menekan tombol *Yes*, sistem menembak *endpoint* API DELETE.
4. Jika berhasil, sistem otomatis melakukan `location.reload()`.

---

## 4. Keamanan & Pengembangan Berkelanjutan

### A. Proactive Review & Security
Di setiap penambahan modul, hal-hal berikut wajib ditinjau:
1. Validasi ganda (Frontend dan Backend) sebelum merekam data ke *database*.
2. Mempertimbangkan pendekatan **Soft Delete** pada data krusial keuangan dan siswa (mengubah kolom `status` alih-alih menghapus catatan di *database* secara keras).

### B. Git Milestones (Version Control)
Kode sumber (Source code) dikontrol ketat menggunakan **Git**.
- Setiap tercapai suatu fase kestabilan sistem (seperti penyelesaian *refactoring* UI atau modul besar), titik koordinat tersebut wajib "dikunci" menggunakan **Git Tag** (contoh: `v1.0-stable-auth-ui`).
- *Tag* ini berfungsi sebagai titik sandar (Safety Net/Titik Pulih) jika kelak sistem mengalami kerusakan (*bug*) akut di masa depan akibat eksperimen fitur baru.
