
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.page_login, name='page_login'),
    path('register/', views.page_register, name='page_register'),
    path('forgot-password/', views.page_forgot_password, name='page_forgot_password'),
    path('page-register/', views.page_register, name='page-register'),
    path('page-forgot-password/', views.page_forgot_password, name='page-forgot-password'),
    path('logout/', views.page_logout, name='page_logout'),
    path('app-profile/', views.app_profile, name='app-profile'),
    path('registrasi-siswa/', views.registrasi_siswa, name='registrasi_siswa'),
    path('enrollment-siswa/', views.enrollment_siswa, name='enrollment_siswa'),
    path('master-cabang/', views.master_cabang, name='master_cabang'),
    path('master-ruangan/', views.master_ruangan, name='master_ruangan'),
    path('master-kursus/', views.master_kursus, name='master_kursus'),
    path('master-level/', views.master_level, name='master_level'),

    path('master-hari-libur/', views.master_hari_libur, name='master_hari_libur'),
    path('master-alasan-absen/', views.master_alasan_absen, name='master_alasan_absen'),
    path('master-metode-bayar/', views.master_metode_bayar, name='master_metode_bayar'),
    path('master-kategori-biaya/', views.master_kategori_biaya, name='master_kategori_biaya'),
    path('master-jabatan/', views.master_jabatan, name='master_jabatan'),
    path('master-status-prospek/', views.master_status_prospek, name='master_status_prospek'),
    path('master-karyawan/', views.master_karyawan, name='master_karyawan'),
    path('master-tahun-ajaran/', views.master_tahun_ajaran, name='master_tahun_ajaran'),
    path('master-paket-edukasi/', views.master_paket_edukasi, name='master_paket_edukasi'),
    path('billing/', views.billing_index, name='billing_index'),
    path('validasi-pembayaran/', views.validasi_pembayaran, name='validasi_pembayaran'),
    path('404/', views.page_error_404, name='page_error_404'),
]

