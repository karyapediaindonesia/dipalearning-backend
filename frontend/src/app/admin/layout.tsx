import React from 'react';
import Sidebar from '@/components/Sidebar/Sidebar';
import styles from './adminLayout.module.css';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className={styles.layout}>
            <Sidebar />
            <div className={styles.mainContent}>
                {children}
            </div>
        </div>
    );
}
