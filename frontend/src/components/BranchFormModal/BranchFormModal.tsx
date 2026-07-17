'use client';

import React, { useState, useEffect } from 'react';
import { createBranch, updateBranch } from '@/services/branches';
import styles from './BranchFormModal.module.css';

interface BranchFormModalProps {
    branch?: any;
    onClose: () => void;
    onSuccess: () => void;
}

export default function BranchFormModal({ branch, onClose, onSuccess }: BranchFormModalProps) {
    const [activeTab, setActiveTab] = useState(0);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        // Identitas
        code: '',
        name: '',
        short_name: '',
        branch_type: 'BRANCH',
        parent_branch: '',
        
        // Alamat
        address: '',
        province: '',
        city: '',
        district: '',
        sub_district: '',
        postal_code: '',
        map_location: '',
        
        // Kontak
        phone_number: '',
        whatsapp_number: '',
        email: '',
        person_in_charge: '',
        
        // Administrasi
        timezone: 'Asia/Jakarta',
        operational_date: '',
        status: 'ACTIVE',
        status_effective_date: '',
        deactivation_reason: '',
        notes: ''
    });

    useEffect(() => {
        if (branch) {
            setFormData({
                ...formData,
                ...branch,
                parent_branch: branch.parent_branch || '',
                person_in_charge: branch.person_in_charge || '',
            });
        }
    }, [branch]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            // Remove empty fields that might cause issues for foreign keys or dates
            const payload: any = { ...formData };
            if (!payload.parent_branch) delete payload.parent_branch;
            if (!payload.person_in_charge) delete payload.person_in_charge;
            if (!payload.operational_date) delete payload.operational_date;
            if (!payload.status_effective_date) delete payload.status_effective_date;

            if (branch && branch.id) {
                await updateBranch(branch.id, payload);
            } else {
                await createBranch(payload);
            }
            onSuccess();
        } catch (error) {
            console.error(error);
            alert('Terjadi kesalahan saat menyimpan data.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.modalOverlay}>
            <div className={styles.modalContent}>
                <div className={styles.header}>
                    <h2>{branch ? 'Edit Master Cabang' : 'Tambah Master Cabang'}</h2>
                    <button className={styles.closeButton} onClick={onClose}>&times;</button>
                </div>
                
                <div className={styles.tabs}>
                    <button className={`${styles.tab} ${activeTab === 0 ? styles.activeTab : ''}`} onClick={() => setActiveTab(0)}>
                        1. Identitas Cabang
                    </button>
                    <button className={`${styles.tab} ${activeTab === 1 ? styles.activeTab : ''}`} onClick={() => setActiveTab(1)}>
                        2. Alamat Cabang
                    </button>
                    <button className={`${styles.tab} ${activeTab === 2 ? styles.activeTab : ''}`} onClick={() => setActiveTab(2)}>
                        3. Kontak & PIC
                    </button>
                    <button className={`${styles.tab} ${activeTab === 3 ? styles.activeTab : ''}`} onClick={() => setActiveTab(3)}>
                        4. Status & Admin
                    </button>
                </div>

                <form onSubmit={handleSubmit} className={styles.formBody}>
                    {activeTab === 0 && (
                        <div className={styles.grid}>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Kode Cabang <span style={{color:'red'}}>*</span></label>
                                <input required className={styles.input} name="code" value={formData.code} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Nama Cabang <span style={{color:'red'}}>*</span></label>
                                <input required className={styles.input} name="name" value={formData.name} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Nama Singkat</label>
                                <input className={styles.input} name="short_name" value={formData.short_name} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Jenis Cabang <span style={{color:'red'}}>*</span></label>
                                <select required className={styles.select} name="branch_type" value={formData.branch_type} onChange={handleChange}>
                                    <option value="HEAD_OFFICE">Kantor Pusat</option>
                                    <option value="BRANCH">Cabang</option>
                                    <option value="SUB_BRANCH">Cabang Pembantu</option>
                                </select>
                            </div>
                            <div className={`${styles.formGroup} ${styles.fullWidth}`}>
                                <label className={styles.label}>Cabang Induk (Opsional)</label>
                                <input className={styles.input} name="parent_branch" value={formData.parent_branch} onChange={handleChange} placeholder="Masukkan ID cabang induk..." />
                            </div>
                        </div>
                    )}

                    {activeTab === 1 && (
                        <div className={styles.grid}>
                            <div className={`${styles.formGroup} ${styles.fullWidth}`}>
                                <label className={styles.label}>Alamat Lengkap <span style={{color:'red'}}>*</span></label>
                                <textarea required className={styles.textarea} name="address" value={formData.address} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Provinsi <span style={{color:'red'}}>*</span></label>
                                <input required className={styles.input} name="province" value={formData.province} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Kota / Kabupaten <span style={{color:'red'}}>*</span></label>
                                <input required className={styles.input} name="city" value={formData.city} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Kecamatan</label>
                                <input className={styles.input} name="district" value={formData.district} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Kelurahan / Desa</label>
                                <input className={styles.input} name="sub_district" value={formData.sub_district} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Kode Pos</label>
                                <input className={styles.input} name="postal_code" value={formData.postal_code} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Lokasi Peta (URL/Kordinat)</label>
                                <input className={styles.input} name="map_location" value={formData.map_location} onChange={handleChange} />
                            </div>
                        </div>
                    )}

                    {activeTab === 2 && (
                        <div className={styles.grid}>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Nomor Telepon <span style={{color:'red'}}>*</span></label>
                                <input required className={styles.input} name="phone_number" value={formData.phone_number} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Nomor WhatsApp</label>
                                <input className={styles.input} name="whatsapp_number" value={formData.whatsapp_number} onChange={handleChange} />
                            </div>
                            <div className={`${styles.formGroup} ${styles.fullWidth}`}>
                                <label className={styles.label}>Email Cabang</label>
                                <input type="email" className={styles.input} name="email" value={formData.email} onChange={handleChange} />
                            </div>
                            <div className={`${styles.formGroup} ${styles.fullWidth}`}>
                                <label className={styles.label}>Penanggung Jawab (ID User)</label>
                                <input className={styles.input} name="person_in_charge" value={formData.person_in_charge} onChange={handleChange} placeholder="Masukkan ID User PIC..." />
                            </div>
                            {branch && branch.pic_position && (
                                <div className={styles.formGroup}>
                                    <label className={styles.label}>Jabatan PIC (Otomatis)</label>
                                    <input className={styles.input} value={branch.pic_position} disabled />
                                </div>
                            )}
                            {branch && branch.pic_contact && (
                                <div className={styles.formGroup}>
                                    <label className={styles.label}>Kontak PIC (Otomatis)</label>
                                    <input className={styles.input} value={branch.pic_contact} disabled />
                                </div>
                            )}
                        </div>
                    )}

                    {activeTab === 3 && (
                        <div className={styles.grid}>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Zona Waktu <span style={{color:'red'}}>*</span></label>
                                <select required className={styles.select} name="timezone" value={formData.timezone} onChange={handleChange}>
                                    <option value="Asia/Jakarta">WIB (Asia/Jakarta)</option>
                                    <option value="Asia/Makassar">WITA (Asia/Makassar)</option>
                                    <option value="Asia/Jayapura">WIT (Asia/Jayapura)</option>
                                </select>
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Tanggal Mulai Operasional</label>
                                <input type="date" className={styles.input} name="operational_date" value={formData.operational_date} onChange={handleChange} />
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Status Cabang <span style={{color:'red'}}>*</span></label>
                                <select required className={styles.select} name="status" value={formData.status} onChange={handleChange}>
                                    <option value="ACTIVE">Aktif</option>
                                    <option value="INACTIVE">Nonaktif</option>
                                    <option value="CLOSED">Tutup</option>
                                </select>
                            </div>
                            <div className={styles.formGroup}>
                                <label className={styles.label}>Tanggal Efektif Status</label>
                                <input type="date" className={styles.input} name="status_effective_date" value={formData.status_effective_date} onChange={handleChange} />
                            </div>
                            <div className={`${styles.formGroup} ${styles.fullWidth}`}>
                                <label className={styles.label}>Alasan Nonaktif / Penutupan</label>
                                <textarea className={styles.textarea} name="deactivation_reason" value={formData.deactivation_reason} onChange={handleChange} />
                            </div>
                            <div className={`${styles.formGroup} ${styles.fullWidth}`}>
                                <label className={styles.label}>Catatan</label>
                                <textarea className={styles.textarea} name="notes" value={formData.notes} onChange={handleChange} />
                            </div>
                        </div>
                    )}
                </form>
                
                <div className={styles.footer}>
                    <button type="button" className={styles.cancelBtn} onClick={onClose}>Batal</button>
                    <button type="button" className={styles.submitBtn} disabled={loading} onClick={handleSubmit}>
                        {loading ? 'Menyimpan...' : 'Simpan Data Cabang'}
                    </button>
                </div>
            </div>
        </div>
    );
}
