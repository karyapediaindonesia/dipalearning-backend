# Information Architecture (IA) - SIM DIPA Learning Center

Information Architecture ini mendefinisikan struktur, navigasi, dan hierarki menu dari Sistem Informasi Manajemen DIPA Learning Center berdasarkan modul-modul fungsional dan Role-Based Access Control (RBAC).

## 1. Struktur Global (Semua Role)

Struktur ini merepresentasikan kerangka utama dari aplikasi, di mana menu yang terlihat akan menyesuaikan dengan hak akses (permission) dari masing-masing role pengguna yang sedang login.

```text
[Aplikasi SIM DIPA]
├── Halaman Autentikasi
│   ├── Login
│   ├── Lupa Password
│   └── Reset Password
├── Dashboard (Beranda Utama - Disesuaikan per Role)
├── Menu Navigasi Utama (Sidebar/Top Nav)
│   ├── 1. Akademik & Kelas
│   ├── 2. Registrasi & Siswa
│   ├── 3. Keuangan & Tagihan
│   ├── 4. Presensi (Kehadiran)
│   ├── 5. HR & Payroll
│   ├── 6. Inventaris & Logistik
│   ├── 7. Laporan & Analitik
│   └── 8. Pengaturan Sistem
└── Profil Pengguna
    ├── Lihat Profil Aktif (Cabang, Role, Izin)
    ├── Ganti Password
    └── Logout
```

---

## 2. Peta Menu Berdasarkan Modul

### 1. Akademik & Kelas (Academic)
- **Master Data Akademik**
  - Daftar Kursus (Courses)
  - Tingkatan / Level
  - Kurikulum / Modul Belajar
- **Jadwal & Kelas**
  - Daftar Kelas Aktif
  - Jadwal Reguler (Occurrence)
  - Permintaan Make-up Class
- **Penugasan Coach**
  - Jadwal Mengajar Coach

### 2. Registrasi & Siswa (Student Management)
- **Data Siswa**
  - Direktori Siswa
  - Profil Lengkap Siswa (Riwayat Kursus, Transaksi, Kuota, Presensi)
- **Pendaftaran (Enrollment)**
  - Pendaftaran Siswa Baru
  - Pendaftaran Kursus/Kelas Baru (Siswa Lama)
- **Manajemen Kuota**
  - Status Kuota per Siswa (Aktif, Kedaluwarsa, Habis)

### 3. Keuangan & Tagihan (Billing & Finance)
- **Master Keuangan**
  - Price List (Harga Paket, Diskon)
- **Tagihan (Billing)**
  - Daftar Invoice (Lunas, Belum Lunas, Kedaluwarsa)
  - Buat Invoice Baru (Manual / Auto dari Pendaftaran)
- **Pembayaran (Payment)**
  - Verifikasi Pembayaran / Konfirmasi Transfer
  - Kas & Bank (Buku Kas Cabang)
  - Rekonsiliasi Jurnal (General Ledger)

### 4. Presensi / Kehadiran (Attendance)
- **Dashboard Presensi Harian**
- **Check-in / Kedatangan** (Admin Depan)
- **Validasi Masuk Kelas** (Coach)
- **Checkout / Pulang** (Admin Belakang)
- **Riwayat Absensi Siswa**

### 5. HR & Payroll
- **Data Pegawai**
  - Direktori Staff & Coach
- **Payroll (Penggajian)**
  - Perhitungan Strata / Formula Gaji Coach
  - Meeting Percentage (Rekap Mengajar)
  - Approval Payroll
  - Riwayat Pembayaran Gaji

### 6. Inventaris & Logistik (Inventory)
- **Katalog Barang**
  - Daftar Inventaris & Modul Fisik
- **Manajemen Stok**
  - Stok Masuk (Inbound)
  - Stok Keluar (Outbound)
  - Transfer Antar Cabang
  - Stock Opname (Penyesuaian Fisik)

### 7. Laporan & Analitik (Reporting)
- **Laporan Operasional**
  - Laporan Absensi & Penggunaan Kuota
  - Laporan Kelas & Make-up Class
- **Laporan Keuangan**
  - Laporan Pendapatan & Invoice
  - Laporan Kas & Pengeluaran
- **Laporan Inventaris**
  - Kartu Stok & Pergerakan Barang

### 8. Pengaturan Sistem (Settings & RBAC)
- **Manajemen Cabang (Branch)**
  - Daftar Cabang Operasional
- **Manajemen Pengguna (Users)**
  - Daftar Akun Pengguna
- **Manajemen Role & Permission**
  - Daftar Peran (Super Admin, Branch Manager, Admin Depan, dll)
  - Mapping Izin Akses (Create, Read, Update, Delete)
- **Audit Trail (Log Aktivitas)**
- **Pengaturan Umum Aplikasi**

---

## 3. Information Architecture Berdasarkan Role

Aplikasi menggunakan prinsip *RBAC (Role-Based Access Control)*. Berikut adalah *sitemap* atau menu yang relevan berdasarkan aktor/role utama.

### A. Admin Depan (Front Desk)
*Fokus: Operasional harian di resepsionis, penerimaan tamu/siswa, pendaftaran, dan check-in.*
- **Dashboard**: Ringkasan jadwal kelas hari ini, jumlah kedatangan.
- **Registrasi & Siswa**: Pendaftaran siswa baru, pencarian profil siswa.
- **Keuangan & Tagihan**: Pembuatan invoice awal, cetak kuitansi.
- **Presensi**: Layar Check-in siswa (kedatangan).
- **Inventaris**: Penjualan merchandise/modul ringan (stok keluar).

### B. Coach (Pengajar)
*Fokus: Pengajaran, presensi di dalam kelas, dan jadwal pribadi.*
- **Dashboard**: Jadwal mengajar hari ini, notifikasi kelas pengganti.
- **Akademik & Kelas**: Daftar kelas yang diajar, materi pelajaran.
- **Presensi**: Layar validasi kehadiran siswa masuk kelas (mencocokkan siswa yang sudah check-in).
- **Profil & HR**: Rekap meeting percentage, riwayat payroll/insentif pribadi.

### C. Admin Belakang (Back Office / Admin Akademik & Keuangan)
*Fokus: Validasi data, keuangan, pengaturan jadwal, inventaris cabang, dan checkout siswa.*
- **Dashboard**: Ringkasan invoice pending, permintaan make-up class, stok menipis.
- **Akademik & Kelas**: Pengelolaan kelas, jadwal reguler, memproses permintaan make-up class.
- **Keuangan & Tagihan**: Verifikasi bukti pembayaran, rekonsiliasi kas cabang.
- **Presensi**: Layar Checkout siswa (pulang), koreksi absensi.
- **Inventaris**: Penerimaan barang (stok masuk), stock opname cabang.
- **Laporan**: Laporan operasional cabang (keuangan dasar, kehadiran).

### D. Branch Manager (Manager Cabang)
*Fokus: Pengawasan seluruh aktivitas operasional dan finansial di satu cabang.*
- **Dashboard**: Analitik cabang (pendapatan, jumlah siswa aktif, utilisasi kelas).
- **Persetujuan (Approval)**: Approval diskon khusus, approval refund, approval koreksi stok.
- **Laporan & Analitik**: Akses penuh ke seluruh laporan operasional, keuangan, dan inventaris untuk cabang tersebut.
- **HR & Payroll**: Approval awal payroll coach di cabang tersebut sebelum dikirim ke pusat.

### E. Super Admin (Owner / HQ)
*Fokus: Pengendalian penuh seluruh sistem, multi-cabang, konfigurasi global.*
- **Dashboard Eksekutif**: Konsolidasi data dari seluruh cabang (Target ekspansi 7 cabang).
- **Pengaturan Sistem (Full Access)**: Manajemen Role, Permission, Cabang, Audit Trail.
- **HR & Payroll (HQ)**: Perhitungan final payroll, manajemen master data pegawai.
- **Laporan (Cross-Branch)**: Laporan komprehensif, rekonsiliasi general ledger.
- *Memiliki akses ke seluruh menu yang ada pada sistem tanpa batasan branch (ALL_BRANCHES).*
