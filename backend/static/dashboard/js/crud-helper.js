// Fungsi untuk mengambil cookie berdasarkan namanya, khususnya CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Cek apakah awalan cookie sesuai dengan nama yang dicari
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Menampilkan modal konfirmasi SweetAlert dan melakukan penghapusan data via DELETE API.
 * 
 * @param {string} url - URL lengkap dari endpoint API untuk DELETE
 * @param {string} itemName - Nama item yang akan dihapus untuk ditampilkan di pesan konfirmasi
 * @param {function} [onSuccess] - Callback kustom bila penghapusan sukses. Default: location.reload()
 */
function hapusData(url, itemName, onSuccess) {
    Swal.fire({
        title: 'Konfirmasi',
        text: `Yakin ingin menghapus ${itemName}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Ya, hapus!',
        cancelButtonText: 'Batal'
    }).then((result) => {
        if (result.value) {
            fetch(url, {
                method: 'DELETE',
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            }).then(r => {
                if (r.ok) {
                    Swal.fire('Terhapus!', 'Data telah dihapus.', 'success').then(() => {
                        if (typeof onSuccess === 'function') {
                            onSuccess();
                        } else {
                            location.reload();
                        }
                    });
                } else {
                    r.json().then(json => {
                        let errMsg = 'Gagal menghapus data.';
                        if (typeof json === 'object' && !Array.isArray(json)) {
                            errMsg = Object.values(json).join('\n');
                        } else {
                            errMsg = json.detail || json[0] || errMsg;
                        }
                        Swal.fire('Gagal!', errMsg, 'error');
                    }).catch(() => Swal.fire('Error!', 'Gagal menghapus data. Status: ' + r.status, 'error'));
                }
            }).catch(() => Swal.fire('Error!', 'Terjadi kesalahan jaringan.', 'error'));
        }
    });
}
