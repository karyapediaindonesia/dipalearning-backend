'use client';
import React, { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { updateMe, API_URL } from '@/services/auth';
import styles from './EditProfileModal.module.css';

const getPhotoUrl = (photoPath: any) => {
    try {
        if (!photoPath || typeof photoPath !== 'string') return 'none';
        if (photoPath.startsWith('http') || photoPath.startsWith('blob:')) return `url(${photoPath})`;
        const baseUrl = API_URL ? API_URL.split('/api')[0] : '';
        return `url(${baseUrl}${photoPath})`;
    } catch (e) {
        return 'none';
    }
};

interface EditProfileModalProps {
    user: any;
    onClose: () => void;
    onSuccess: (updatedUser: any) => void;
}

export default function EditProfileModal({ user, onClose, onSuccess }: EditProfileModalProps) {
    const [firstName, setFirstName] = useState(user.first_name || '');
    const [lastName, setLastName] = useState(user.last_name || '');
    const [email, setEmail] = useState(user.email || '');
    const [photoFile, setPhotoFile] = useState<File | null>(null);
    const [photoPreview, setPhotoPreview] = useState<string | null>(user.photo || null);
    
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setPhotoFile(file);
            setPhotoPreview(URL.createObjectURL(file));
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const formData = new FormData();
            formData.append('first_name', firstName);
            formData.append('last_name', lastName);
            formData.append('email', email);
            
            if (photoFile) {
                formData.append('photo', photoFile);
            }

            const updatedUser = await updateMe(formData);
            onSuccess(updatedUser);
        } catch (err: any) {
            setError(err.message || 'Failed to update profile');
        } finally {
            setLoading(false);
        }
    };

    const modalContent = (
        <div className={styles.overlay} onClick={onClose}>
            <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
                <div className={styles.header}>
                    <h2>Edit Profile</h2>
                    <button className={styles.closeBtn} onClick={onClose}>&times;</button>
                </div>
                
                <form className={styles.form} onSubmit={handleSubmit}>
                    {error && <div className={styles.error}>{error}</div>}
                    
                    <div className={styles.avatarSection}>
                        <div 
                            className={styles.avatarPreview} 
                            style={{ backgroundImage: getPhotoUrl(photoPreview) }}
                            onClick={() => fileInputRef.current?.click()}
                        >
                            {!photoPreview && <span>Upload</span>}
                        </div>
                        <input 
                            type="file" 
                            accept="image/*" 
                            ref={fileInputRef} 
                            style={{ display: 'none' }} 
                            onChange={handleFileChange} 
                        />
                        <button type="button" className={styles.uploadBtn} onClick={() => fileInputRef.current?.click()}>
                            Change Photo
                        </button>
                    </div>

                    <div className={styles.inputGroup}>
                        <label>First Name</label>
                        <input 
                            type="text" 
                            value={firstName} 
                            onChange={(e) => setFirstName(e.target.value)} 
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label>Last Name</label>
                        <input 
                            type="text" 
                            value={lastName} 
                            onChange={(e) => setLastName(e.target.value)} 
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label>Email</label>
                        <input 
                            type="email" 
                            value={email} 
                            onChange={(e) => setEmail(e.target.value)} 
                            required 
                        />
                    </div>

                    <div className={styles.actions}>
                        <button type="button" className={styles.cancelBtn} onClick={onClose}>Cancel</button>
                        <button type="submit" className={styles.saveBtn} disabled={loading}>
                            {loading ? 'Saving...' : 'Save Changes'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );

    // Only render portal on the client side
    const [mounted, setMounted] = useState(false);
    useEffect(() => setMounted(true), []);

    if (!mounted) return null;
    return createPortal(modalContent, document.body);
}
