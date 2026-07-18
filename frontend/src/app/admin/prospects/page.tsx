'use client';

import React, { useEffect, useState } from 'react';
import { getProspects, deleteProspect } from '@/services/prospects';
import styles from './prospects.module.css';
import ProspectFormModal from '@/components/ProspectFormModal/ProspectFormModal';
import DeleteConfirmModal from '@/components/DeleteConfirmModal/DeleteConfirmModal';

export default function ProspectsPage() {
    const [prospects, setProspects] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingProspect, setEditingProspect] = useState<any>(null);
    const [deletingProspect, setDeletingProspect] = useState<any>(null);

    const fetchProspects = async () => {
        setLoading(true);
        try {
            const data = await getProspects();
            setProspects(data);
        } catch (error) {
            console.error('Error fetching prospects:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchProspects();
    }, []);

    const handleDelete = async () => {
        if (deletingProspect) {
            await deleteProspect(deletingProspect.id);
            setDeletingProspect(null);
            fetchProspects();
        }
    };

    const handleEdit = (prospect: any) => {
        setEditingProspect(prospect);
        setIsModalOpen(true);
    };

    const handleAdd = () => {
        setEditingProspect(null);
        setIsModalOpen(true);
    };

    const getStatusStyle = (status: string) => {
        switch(status) {
            case 'NEW': return styles.statusNew;
            case 'CONTACTED': return styles.statusContacted;
            case 'INTERESTED': return styles.statusInterested;
            case 'ENROLLED': return styles.statusEnrolled;
            case 'LOST':
            case 'NOT_INTERESTED':
                return styles.statusLost;
            default: return styles.statusDefault;
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1>Registrasi Calon Siswa (Prospects)</h1>
                <button className={styles.addButton} onClick={handleAdd}>
                    <span>➕</span> Tambah Prospect
                </button>
            </div>

            <div className={styles.tableContainer}>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th>No Prospect</th>
                            <th>Nama Lengkap</th>
                            <th>Jenjang</th>
                            <th>No. Telepon / WA</th>
                            <th>Tanggal Masuk</th>
                            <th>Status</th>
                            <th>Aksi</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loading ? (
                            <tr>
                                <td colSpan={7} style={{ textAlign: 'center' }}>Loading...</td>
                            </tr>
                        ) : prospects.length === 0 ? (
                            <tr>
                                <td colSpan={7} style={{ textAlign: 'center' }}>Tidak ada data prospect.</td>
                            </tr>
                        ) : (
                            prospects.map((prospect) => (
                                <tr key={prospect.id}>
                                    <td><strong>{prospect.prospect_number}</strong></td>
                                    <td>{prospect.full_name}</td>
                                    <td>{prospect.edu_level || '-'}</td>
                                    <td>{prospect.parent?.whatsapp || '-'}</td>
                                    <td>{new Date(prospect.created_at).toLocaleDateString('id-ID')}</td>
                                    <td>
                                        <span className={`${styles.statusBadge} ${getStatusStyle(prospect.status)}`}>
                                            {prospect.status}
                                        </span>
                                    </td>
                                    <td>
                                        <div className={styles.actions}>
                                            <button className={styles.editBtn} onClick={() => handleEdit(prospect)} title="Edit">
                                                ✏️
                                            </button>
                                            <button className={styles.deleteBtn} onClick={() => setDeletingProspect(prospect)} title="Hapus">
                                                🗑️
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {isModalOpen && (
                <ProspectFormModal 
                    prospect={editingProspect} 
                    onClose={() => setIsModalOpen(false)} 
                    onSuccess={() => {
                        setIsModalOpen(false);
                        fetchProspects();
                    }}
                />
            )}

            {deletingProspect && (
                <DeleteConfirmModal
                    title="Hapus Calon Siswa"
                    message={
                        <span>
                            Apakah Anda yakin ingin menghapus calon siswa <strong>{deletingProspect.full_name}</strong>?
                        </span>
                    }
                    itemName={deletingProspect.full_name}
                    onConfirm={handleDelete}
                    onClose={() => setDeletingProspect(null)}
                />
            )}
        </div>
    );
}
