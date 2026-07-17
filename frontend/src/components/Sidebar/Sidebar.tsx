'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import styles from './Sidebar.module.css';

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className={styles.sidebar}>
            <div className={styles.logo}>
                DIPA<span>Learning</span>
            </div>
            <nav className={styles.menu}>
                <div className={styles.menuGroup}>
                    <div className={styles.menuTitle}>Menu Utama</div>
                    <ul className={styles.menuList}>
                        <li>
                            <Link href="/admin/dashboard" className={`${styles.menuItem} ${pathname === '/admin/dashboard' ? styles.active : ''}`}>
                                <span>📊</span> Dashboard
                            </Link>
                        </li>
                    </ul>
                </div>

                <div className={styles.menuGroup}>
                    <div className={styles.menuTitle}>Kesiswaan</div>
                    <ul className={styles.menuList}>
                        <li>
                            <Link href="/admin/prospects" className={`${styles.menuItem} ${pathname.startsWith('/admin/prospects') ? styles.active : ''}`}>
                                <span>📝</span> Registrasi Calon Siswa
                            </Link>
                        </li>
                    </ul>
                </div>

                <div className={styles.menuGroup}>
                    <div className={styles.menuTitle}>Master Data</div>
                    <ul className={styles.menuList}>
                        <li>
                            <Link href="/admin/branches" className={`${styles.menuItem} ${pathname.startsWith('/admin/branches') ? styles.active : ''}`}>
                                <span>🏢</span> Master Cabang
                            </Link>
                        </li>
                    </ul>
                </div>
            </nav>
        </aside>
    );
}
