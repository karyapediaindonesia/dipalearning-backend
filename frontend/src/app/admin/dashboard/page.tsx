'use client';

import React, { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { getMe, logout, API_URL } from '@/services/auth';
import EditProfileModal from '@/components/EditProfileModal/EditProfileModal';
import styles from './dashboard.module.css';

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

export default function AdminDashboard() {
    const router = useRouter();
    const [user, setUser] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const userInfoRef = useRef<HTMLDivElement>(null);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (userInfoRef.current && !userInfoRef.current.contains(event.target as Node)) {
                setIsDropdownOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const userData = await getMe();
                setUser(userData);
            } catch (err) {
                // Token invalid or no token, redirect to login
                router.push('/auth/login');
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, [router]);

    const handleLogout = () => {
        logout();
        router.push('/auth/login');
    };

    if (loading) {
        return (
            <div className={styles.loadingContainer}>
                <div className={styles.loader}></div>
                <p>Loading your dashboard...</p>
            </div>
        );
    }

    if (!user) return null;

    return (
        <div className={styles.container}>
            <header className={styles.header}>
                <div className={styles.logo}>
                    Admin<span>Dashboard</span>
                </div>
                <div className={styles.userInfo} ref={userInfoRef}>
                    <div 
                        className={styles.profileSection} 
                        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                        title="Profile Menu"
                    >
                        <div className={styles.avatar} style={{
                            backgroundImage: getPhotoUrl(user.photo),
                            backgroundSize: 'cover',
                            backgroundPosition: 'center',
                            color: user.photo ? 'transparent' : '#4b5563'
                        }}>
                            {!user.photo && (user.first_name ? user.first_name[0].toUpperCase() : user.username[0].toUpperCase())}
                        </div>
                        <div className={styles.userDetails}>
                            <span className={styles.greeting}>Hi, <strong>{user.first_name || user.username}</strong></span>
                            <span className={styles.email}>{user.email}</span>
                        </div>
                    </div>
                    
                    {isDropdownOpen && (
                        <div className={styles.dropdownMenu}>
                            <button 
                                type="button"
                                className={styles.dropdownItem} 
                                onClick={(e) => { 
                                    e.preventDefault();
                                    e.stopPropagation(); 
                                    setIsEditModalOpen(true); 
                                    setTimeout(() => setIsDropdownOpen(false), 100);
                                }}
                            >
                                <span className={styles.iconProfile}>👤</span> Profile
                            </button>
                            <button 
                                type="button"
                                className={styles.dropdownItem} 
                                onClick={(e) => { e.stopPropagation(); setIsDropdownOpen(false); /* Navigate to inbox */ }}
                            >
                                <span className={styles.iconInbox}>✉️</span> Inbox
                            </button>
                            <button 
                                type="button"
                                className={styles.dropdownItem} 
                                onClick={(e) => { e.stopPropagation(); setIsDropdownOpen(false); handleLogout(); }}
                            >
                                <span className={styles.iconLogout}>🚪</span> Logout
                            </button>
                        </div>
                    )}
                </div>
            </header>

            <main className={styles.main}>
                <div className={styles.welcomeCard}>
                    <h1>Welcome back, {user.first_name || 'Admin'}!</h1>
                    <p>Here's what's happening with your projects today.</p>
                </div>

                <div className={styles.statsGrid}>
                    <div className={styles.statCard}>
                        <h3>Total Users</h3>
                        <p className={styles.statNumber}>1,024</p>
                    </div>
                    <div className={styles.statCard}>
                        <h3>Active Branches</h3>
                        <p className={styles.statNumber}>12</p>
                    </div>
                    <div className={styles.statCard}>
                        <h3>Roles Configured</h3>
                        <p className={styles.statNumber}>4</p>
                    </div>
                </div>
                
                <div className={styles.detailsCard}>
                    <h2>Your Account Details</h2>
                    <ul className={styles.detailsList}>
                        <li><strong>Email:</strong> {user.email}</li>
                        <li><strong>Username:</strong> {user.username}</li>
                        <li><strong>Status:</strong> {user.is_active ? 'Active' : 'Inactive'}</li>
                        <li><strong>Joined:</strong> {new Date(user.date_joined).toLocaleDateString()}</li>
                    </ul>
                </div>
            </main>

            {isEditModalOpen && (
                <EditProfileModal 
                    user={user} 
                    onClose={() => setIsEditModalOpen(false)} 
                    onSuccess={(updatedUser) => {
                        setUser(updatedUser);
                        setIsEditModalOpen(false);
                    }} 
                />
            )}
        </div>
    );
}
