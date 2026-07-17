# SIM-DIPA (Sistem Informasi Manajemen DIPA Learning Center)

## Persyaratan Sistem (Windows)
1. **Python 3.12+**
2. **Node.js 20+**
3. **PostgreSQL 14+**
4. **Git**

## Panduan Instalasi (Windows)

### 1. Kloning Repositori
```powershell
git clone <url-repo>
cd dipalearning
```

### 2. Setup Backend (Django)
Buka PowerShell atau Command Prompt:
```powershell
cd backend

# Membuat dan mengaktifkan virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # (Jika menggunakan PowerShell)

# Install dependensi
pip install -r requirements\base.txt

# Menyiapkan konfigurasi environment
Copy-Item .env.example .env.dev
# Edit .env.dev dengan kredensial database PostgreSQL Anda

# Migrasi Database
python manage.py migrate

# Menjalankan server
python manage.py runserver
```

### 3. Setup Frontend (Next.js)
Buka terminal baru:
```powershell
cd frontend

# Install package
npm install

# Menyiapkan konfigurasi environment
Copy-Item .env.example .env
# Pastikan NEXT_PUBLIC_API_URL mengarah ke backend (localhost:8000)

# Menjalankan development server
npm run dev
```
