'use client';

import React, { useState } from 'react';
import styles from './DeleteConfirmModal.module.css';

interface DeleteConfirmModalProps {
    title: string;
    message: React.ReactNode;
    confirmText?: string;
    cancelText?: string;
    onConfirm: () => Promise<void>;
    onClose: () => void;
    itemName?: string;
}

export default function DeleteConfirmModal({
    title,
    message,
    confirmText = 'Hapus',
    cancelText = 'Batal',
    onConfirm,
    onClose,
    itemName
}: DeleteConfirmModalProps) {
    const [confirmInput, setConfirmInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleConfirm = async () => {
        if (itemName && confirmInput !== 'HAPUS') {
            setError('Silakan ketik HAPUS untuk mengonfirmasi.');
            return;
        }
        setLoading(true);
        setError(null);
        try {
            await onConfirm();
        } catch (err: any) {
            setError(err.message || 'Gagal menghapus data.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.overlay} onClick={onClose}>
            <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
                <div className={styles.iconContainer}>
                    <svg className={styles.warningIcon} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 9V14M12 17.01L12.01 16.89M12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2Z" 
                              stroke="#ef4444" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                </div>
                
                <h3 className={styles.title}>{title}</h3>
                <div className={styles.message}>{message}</div>
                
                {itemName && (
                    <div className={styles.confirmSection}>
                        <label className={styles.label}>
                            Ketik <span className={styles.keyword}>HAPUS</span> untuk mengonfirmasi tindakan ini:
                        </label>
                        <input
                            type="text"
                            className={styles.input}
                            value={confirmInput}
                            onChange={(e) => {
                                setConfirmInput(e.target.value);
                                setError(null);
                            }}
                            placeholder="HAPUS"
                            disabled={loading}
                        />
                    </div>
                )}

                {error && <div className={styles.error}>{error}</div>}

                <div className={styles.actions}>
                    <button className={styles.cancelBtn} onClick={onClose} disabled={loading}>
                        {cancelText}
                    </button>
                    <button 
                        className={styles.deleteBtn} 
                        onClick={handleConfirm} 
                        disabled={loading || (itemName !== undefined && confirmInput !== 'HAPUS')}
                    >
                        {loading ? <span className={styles.spinner}></span> : confirmText}
                    </button>
                </div>
            </div>
        </div>
    );
}
