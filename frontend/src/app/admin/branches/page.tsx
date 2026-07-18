'use client';

import React, { useEffect, useState } from 'react';
import { getBranches, deleteBranch } from '@/services/branches';
import styles from './branches.module.css';
import BranchFormModal from '@/components/BranchFormModal/BranchFormModal';
import DeleteConfirmModal from '@/components/DeleteConfirmModal/DeleteConfirmModal';

export default function BranchesPage() {
    const [branches, setBranches] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingBranch, setEditingBranch] = useState<any>(null);
    const [deletingBranch, setDeletingBranch] = useState<any>(null);

    const fetchBranches = async () => {
        setLoading(true);
        try {
            const data = await getBranches();
            setBranches(data);
        } catch (error) {
            console.error('Error fetching branches:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchBranches();
    }, []);

    const handleDelete = async () => {
        if (deletingBranch) {
            await deleteBranch(deletingBranch.id);
            setDeletingBranch(null);
            fetchBranches();
        }
    };

    const handleEdit = (branch: any) => {
        setEditingBranch(branch);
        setIsModalOpen(true);
    };

    const handleAdd = () => {
        setEditingBranch(null);
        setIsModalOpen(true);
    };

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1>Master Cabang</h1>
                <button className={styles.addButton} onClick={handleAdd}>
                    <span>➕</span> Tambah Cabang
                </button>
            </div>

            <div className={styles.tableContainer}>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th>Kode</th>
                            <th>Nama Cabang</th>
                            <th>Jenis</th>
                            <th>Kota</th>
                            <th>No. Telepon</th>
                            <th>Status</th>
                            <th>Aksi</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loading ? (
                            <tr>
                                <td colSpan={7} style={{ textAlign: 'center' }}>Loading...</td>
                            </tr>
                        ) : branches.length === 0 ? (
                            <tr>
                                <td colSpan={7} style={{ textAlign: 'center' }}>Tidak ada data cabang.</td>
                            </tr>
                        ) : (
                            branches.map((branch) => (
                                <tr key={branch.id}>
                                    <td><strong>{branch.code}</strong></td>
                                    <td>{branch.name}</td>
                                    <td>
                                        {branch.branch_type === 'HEAD_OFFICE' ? 'Kantor Pusat' :
                                         branch.branch_type === 'BRANCH' ? 'Cabang' : 'Cabang Pembantu'}
                                    </td>
                                    <td>{branch.city || '-'}</td>
                                    <td>{branch.phone_number || '-'}</td>
                                    <td>
                                        <span className={`${styles.statusBadge} ${
                                            branch.status === 'ACTIVE' ? styles.statusActive : 
                                            branch.status === 'INACTIVE' ? styles.statusInactive : styles.statusClosed
                                        }`}>
                                            {branch.status === 'ACTIVE' ? 'Aktif' : 
                                             branch.status === 'INACTIVE' ? 'Nonaktif' : 'Tutup'}
                                        </span>
                                    </td>
                                    <td>
                                        <div className={styles.actions}>
                                            <button className={styles.editBtn} onClick={() => handleEdit(branch)} title="Edit">
                                                ✏️
                                            </button>
                                             <button className={styles.deleteBtn} onClick={() => setDeletingBranch(branch)} title="Hapus">
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
                <BranchFormModal 
                    branch={editingBranch} 
                    onClose={() => setIsModalOpen(false)} 
                    onSuccess={() => {
                        setIsModalOpen(false);
                        fetchBranches();
                    }}
                />
            )}

            {deletingBranch && (
                <DeleteConfirmModal
                    title="Hapus Cabang"
                    message={
                        <span>
                            Apakah Anda yakin ingin menghapus cabang <strong>{deletingBranch.name}</strong>?
                            <br />
                            Tindakan ini akan menonaktifkan cabang dan semua ruangan serta liburan terkait.
                        </span>
                    }
                    itemName={deletingBranch.name}
                    onConfirm={handleDelete}
                    onClose={() => setDeletingBranch(null)}
                />
            )}
        </div>
    );
}
