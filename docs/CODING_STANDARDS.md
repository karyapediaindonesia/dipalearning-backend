# Coding Standards & Guidelines (SIM-DIPA)

## 1. Naming Conventions (Django Apps)
- Gunakan format **plural** (jamak) dan **snake_case** untuk nama aplikasi.
- Contoh: users, invoices, ttendances, payrolls.
- Aplikasi ditempatkan di dalam folder pps/.
- Nama model class menggunakan **PascalCase** dan bentuk tunggal (singular). Contoh: Invoice, Student.
- Nama tabel database akan terbuat secara otomatis oleh Django menggunakan format ppname_modelname.

## 2. Standar Model dan Migration
- Semua model transaksi harus mewarisi pps.core.models.BaseModel yang menyediakan:
  - id: UUID (Primary Key)
  - created_at: DateTime
  - updated_at: DateTime
  - ersion: Integer (Untuk Optimistic Locking)
- Model yang membutuhkan jejak audit pengguna harus mewarisi AuditModel (menambahkan created_by dan updated_by).
- Data master yang tidak boleh dihapus secara permanen (seperti master siswa) harus mewarisi SoftDeleteModel (menambahkan is_active dan deleted_at).

## 3. API Response Standard
Semua respons API akan diformat secara otomatis oleh pps.core.responses.CustomJSONRenderer.
- **Sukses (Single & List)**: Terbungkus dalam "data" dan selalu memiliki "meta" (termasuk correlationId).
- **Error**: Terbungkus dalam "error" (dengan code, message, details, dan correlationId), ditangani oleh custom_exception_handler dari DRF.

## 4. Unit Test Standard
- Unit test ditempatkan di dalam folder 	ests/ pada masing-masing aplikasi atau direktori 	ests/ di root.
- Standar minimum coverage: **80%**.
- Test harus tidak bergantung pada data eksternal (gunakan actory_boy atau Django fixtures).

## 5. Git Branch Strategy
- **main**: Branch utama untuk Production (stabil).
- **develop**: Branch untuk Staging / Integration.
- **feature/[nama-fitur]**: Pembuatan fitur baru (branch dari develop).
- **bugfix/[nama-bug]**: Perbaikan bug di environment staging.
- **hotfix/[nama-hotfix]**: Perbaikan kritis langsung di Production (branch dari main).