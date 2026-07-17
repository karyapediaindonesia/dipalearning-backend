'use client';

import { useEffect, useState } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';
import styles from './PageTransitionLoader.module.css';

export default function PageTransitionLoader() {
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const [loading, setLoading] = useState(true);

    // Initial load & Setiap kali navigasi selesai
    useEffect(() => {
        setLoading(true);
        const timer = setTimeout(() => {
            setLoading(false);
        }, 800);

        return () => clearTimeout(timer);
    }, [pathname, searchParams]);

    if (!loading) return null;

    return (
        <div className={styles.preloader}>
            <div className={styles.waviy}>
                <span style={{ '--i': 1 } as React.CSSProperties}>L</span>
                <span style={{ '--i': 2 } as React.CSSProperties}>o</span>
                <span style={{ '--i': 3 } as React.CSSProperties}>a</span>
                <span style={{ '--i': 4 } as React.CSSProperties}>d</span>
                <span style={{ '--i': 5 } as React.CSSProperties}>i</span>
                <span style={{ '--i': 6 } as React.CSSProperties}>n</span>
                <span style={{ '--i': 7 } as React.CSSProperties}>g</span>
                <span style={{ '--i': 8 } as React.CSSProperties}>.</span>
                <span style={{ '--i': 9 } as React.CSSProperties}>.</span>
                <span style={{ '--i': 10 } as React.CSSProperties}>.</span>
            </div>
        </div>
    );
}
