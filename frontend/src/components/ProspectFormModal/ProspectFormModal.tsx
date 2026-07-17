'use client';

import React, { useState, useEffect } from 'react';
import { createProspect, updateProspect, getProspectOptions } from '@/services/prospects';
import { getBranches } from '@/services/branches';
import styles from './ProspectFormModal.module.css';

interface ProspectFormModalProps {
    prospect?: any;
    onClose: () => void;
    onSuccess: () => void;
}

export default function ProspectFormModal({ prospect, onClose, onSuccess }: ProspectFormModalProps) {
    const [activeTab, setActiveTab] = useState(0);
    const [loading, setLoading] = useState(false);
    
    // Master data state
    const [options, setOptions] = useState<any>({});
    const [branches, setBranches] = useState<any[]>([]);

    const [formData, setFormData] = useState({
        // 1. Data Calon Siswa (Prospect & Address)
        full_name: '', nickname: '', gender: '', place_of_birth: '', date_of_birth: '', nik_nisn: '',
        edu_status: '', school_name: '', edu_level: '', current_class: '', school_entry_year: '',
        current_ability: '', academic_notes: '',
        
        address: { full_address: '', city: '', district: '', postal_code: '' },
        
        // 2. Data Orang Tua (Parent)
        parent: {
            relation: '', full_name: '', gender: '', job: '', company_name: '',
            whatsapp: '', phone: '', email: '', comm_preference: '',
            payer_name: '', payer_relation: '', payment_notes: ''
        },

        // 3. Cabang Tujuan
        target_branch: '', distance_from_home: '', branch_reason: '', alt_branch: '',

        // 4. Sumber Info
        source: { source: '', source_detail: '', campaign: '', referred_by: '' },

        // 5. Minat (Simplification: just one for now, as array)
        interests: [{ course: '', level_estimation: '', package_interest: '', target_start_date: '', interest_notes: '' }],

        // 6. Status
        status: 'NEW', next_followup_date: '', followup_notes: '', lost_reason: ''
    });

    const [calculatedAge, setCalculatedAge] = useState<string>('');

    useEffect(() => {
        const fetchMasterData = async () => {
            try {
                const ops = await getProspectOptions();
                setOptions(ops);
                const br = await getBranches();
                setBranches(br);
            } catch (err) {
                console.error(err);
            }
        };
        fetchMasterData();

        if (prospect) {
            setFormData({
                ...prospect,
                address: prospect.address || { full_address: '', city: '', district: '', postal_code: '' },
                parent: prospect.parent || { relation: '', full_name: '', whatsapp: '' },
                source: prospect.source || { source: '', campaign: '' },
                interests: prospect.interests?.length ? prospect.interests : [{ course: '' }]
            });
            calculateAge(prospect.date_of_birth);
        }
    }, [prospect]);

    const calculateAge = (dobString: string) => {
        if (!dobString) { setCalculatedAge(''); return; }
        const dob = new Date(dobString);
        const diffMs = Date.now() - dob.getTime();
        const ageDt = new Date(diffMs); 
        const years = Math.abs(ageDt.getUTCFullYear() - 1970);
        setCalculatedAge(`${years} Tahun`);
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        
        if (name === 'date_of_birth') {
            calculateAge(value);
        }
    };

    const handleNestedChange = (section: string, field: string, value: string) => {
        setFormData((prev: any) => ({
            ...prev,
            [section]: {
                ...prev[section],
                [field]: value
            }
        }));
    };

    const handleInterestChange = (index: number, field: string, value: string) => {
        const newInterests = [...formData.interests];
        newInterests[index] = { ...newInterests[index], [field]: value };
        setFormData(prev => ({ ...prev, interests: newInterests }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            // Clean up empty nested objects if needed or send as is
            const payload = { ...formData };
            // Ensure foreign keys are passed as ID or null
            if (!payload.target_branch) payload.target_branch = null as any;
            if (!payload.alt_branch) payload.alt_branch = null as any;
            
            if (prospect) {
                await updateProspect(prospect.id, payload);
            } else {
                await createProspect(payload);
            }
            onSuccess();
        } catch (error) {
            console.error(error);
            alert('Terjadi kesalahan saat menyimpan data.');
        } finally {
            setLoading(false);
        }
    };

    const tabs = [
        "Data Calon Siswa", "Orang Tua/Wali", "Cabang Tujuan", "Sumber Info", "Minat Program", "Status"
    ];

    return (
        <div className={styles.overlay}>
            <div className={styles.modal}>
                <div className={styles.header}>
                    <h2>{prospect ? 'Edit Calon Siswa' : 'Tambah Calon Siswa'}</h2>
                    <button className={styles.closeButton} onClick={onClose}>&times;</button>
                </div>
                
                <div className={styles.tabs}>
                    {tabs.map((tab, idx) => (
                        <button 
                            key={idx} 
                            type="button"
                            className={`${styles.tab} ${activeTab === idx ? styles.activeTab : ''}`}
                            onClick={() => setActiveTab(idx)}
                        >
                            {tab}
                        </button>
                    ))}
                </div>

                <form className={styles.content} id="prospectForm" onSubmit={handleSubmit}>
                    
                    {/* TAB 0: Identitas Siswa */}
                    {activeTab === 0 && (
                        <div className={styles.formSection}>
                            <h3>Identitas Dasar</h3>
                            <div className={styles.formRow}>
                                <div className={styles.formGroup}>
                                    <label>Nama Lengkap *</label>
                                    <input required name="full_name" value={formData.full_name} onChange={handleChange} />
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Nama Panggilan</label>
                                    <input name="nickname" value={formData.nickname || ''} onChange={handleChange} />
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Jenis Kelamin *</label>
                                    <select required name="gender" value={formData.gender} onChange={handleChange}>
                                        <option value="">Pilih</option>
                                        {options.gender?.map((o: any) => <option key={o.value} value={o.value}>{o.label}</option>)}
                                    </select>
                                </div>
                                <div className={styles.formGroup}>
                                    <label>NIK/NISN</label>
                                    <input name="nik_nisn" value={formData.nik_nisn || ''} onChange={handleChange} />
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Tanggal Lahir</label>
                                    <input type="date" name="date_of_birth" value={formData.date_of_birth || ''} onChange={handleChange} />
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Usia (Auto Calculate)</label>
                                    <input readOnly value={calculatedAge} style={{backgroundColor: '#f3f4f6'}} />
                                </div>
                            </div>
                            
                            <h3>Informasi Pendidikan</h3>
                            <div className={styles.formRow}>
                                <div className={styles.formGroup}>
                                    <label>Status Pendidikan *</label>
                                    <select required name="edu_status" value={formData.edu_status} onChange={handleChange}>
                                        <option value="">Pilih</option>
                                        {options.edu_status?.map((o: any) => <option key={o.value} value={o.value}>{o.label}</option>)}
                                    </select>
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Jenjang Sekolah *</label>
                                    <select required name="edu_level" value={formData.edu_level} onChange={handleChange}>
                                        <option value="">Pilih</option>
                                        {options.edu_level?.map((o: any) => <option key={o.value} value={o.value}>{o.label}</option>)}
                                    </select>
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Nama Sekolah</label>
                                    <input name="school_name" value={formData.school_name || ''} onChange={handleChange} />
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Kelas Saat Ini</label>
                                    <input name="current_class" value={formData.current_class || ''} onChange={handleChange} />
                                </div>
                            </div>
                        </div>
                    )}

                    {/* TAB 1: Orang Tua */}
                    {activeTab === 1 && (
                        <div className={styles.formSection}>
                            <h3>Identitas Orang Tua</h3>
                            <div className={styles.formRow}>
                                <div className={styles.formGroup}>
                                    <label>Nama Orang Tua/Wali *</label>
                                    <input required value={formData.parent.full_name || ''} onChange={e => handleNestedChange('parent', 'full_name', e.target.value)} />
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Hubungan *</label>
                                    <select required value={formData.parent.relation || ''} onChange={e => handleNestedChange('parent', 'relation', e.target.value)}>
                                        <option value="">Pilih</option>
                                        {options.relation?.map((o: any) => <option key={o.value} value={o.value}>{o.label}</option>)}
                                    </select>
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Nomor WhatsApp *</label>
                                    <input required value={formData.parent.whatsapp || ''} onChange={e => handleNestedChange('parent', 'whatsapp', e.target.value)} />
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Email</label>
                                    <input type="email" value={formData.parent.email || ''} onChange={e => handleNestedChange('parent', 'email', e.target.value)} />
                                </div>
                            </div>

                            <h3>Alamat</h3>
                            <div className={styles.formGroup}>
                                <label>Alamat Lengkap</label>
                                <textarea value={formData.address.full_address || ''} onChange={e => handleNestedChange('address', 'full_address', e.target.value)} rows={3}></textarea>
                            </div>
                            <div className={styles.formRow}>
                                <div className={styles.formGroup}>
                                    <label>Kota</label>
                                    <input value={formData.address.city || ''} onChange={e => handleNestedChange('address', 'city', e.target.value)} />
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Kecamatan</label>
                                    <input value={formData.address.district || ''} onChange={e => handleNestedChange('address', 'district', e.target.value)} />
                                </div>
                            </div>
                        </div>
                    )}

                    {/* TAB 2: Cabang Tujuan */}
                    {activeTab === 2 && (
                        <div className={styles.formSection}>
                            <div className={styles.formGroup}>
                                <label>Cabang Tujuan *</label>
                                <select required name="target_branch" value={formData.target_branch} onChange={handleChange}>
                                    <option value="">Pilih Cabang</option>
                                    {branches.map((b: any) => <option key={b.id} value={b.id}>{b.name}</option>)}
                                </select>
                            </div>
                            <div className={styles.formGroup}>
                                <label>Cabang Alternatif</label>
                                <select name="alt_branch" value={formData.alt_branch} onChange={handleChange}>
                                    <option value="">Pilih Cabang Alternatif</option>
                                    {branches.map((b: any) => <option key={b.id} value={b.id}>{b.name}</option>)}
                                </select>
                            </div>
                            <div className={styles.formGroup}>
                                <label>Alasan Memilih Cabang</label>
                                <input name="branch_reason" value={formData.branch_reason || ''} onChange={handleChange} />
                            </div>
                        </div>
                    )}

                    {/* TAB 3: Sumber Info */}
                    {activeTab === 3 && (
                        <div className={styles.formSection}>
                            <div className={styles.formRow}>
                                <div className={styles.formGroup}>
                                    <label>Sumber Informasi *</label>
                                    <select required value={formData.source.source || ''} onChange={e => handleNestedChange('source', 'source', e.target.value)}>
                                        <option value="">Pilih</option>
                                        {options.source?.map((o: any) => <option key={o.value} value={o.value}>{o.label}</option>)}
                                    </select>
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Campaign</label>
                                    <input value={formData.source.campaign || ''} onChange={e => handleNestedChange('source', 'campaign', e.target.value)} />
                                </div>
                            </div>
                        </div>
                    )}

                    {/* TAB 4: Minat */}
                    {activeTab === 4 && (
                        <div className={styles.formSection}>
                            {formData.interests.map((interest, idx) => (
                                <div key={idx} style={{padding: '16px', border: '1px solid #e5e7eb', borderRadius: '8px', marginBottom: '16px'}}>
                                    <div className={styles.formRow}>
                                        <div className={styles.formGroup}>
                                            <label>Kursus</label>
                                            <input placeholder="ID Kursus atau Nama (Simplifikasi text sementara)" value={interest.course || ''} onChange={e => handleInterestChange(idx, 'course', e.target.value)} />
                                        </div>
                                        <div className={styles.formGroup}>
                                            <label>Level Perkiraan</label>
                                            <input value={interest.level_estimation || ''} onChange={e => handleInterestChange(idx, 'level_estimation', e.target.value)} />
                                        </div>
                                        <div className={styles.formGroup}>
                                            <label>Target Mulai</label>
                                            <input type="date" value={interest.target_start_date || ''} onChange={e => handleInterestChange(idx, 'target_start_date', e.target.value)} />
                                        </div>
                                    </div>
                                    <div className={styles.formGroup} style={{marginTop: '16px'}}>
                                        <label>Catatan Minat</label>
                                        <textarea value={interest.interest_notes || ''} onChange={e => handleInterestChange(idx, 'interest_notes', e.target.value)} rows={2}></textarea>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* TAB 5: Status */}
                    {activeTab === 5 && (
                        <div className={styles.formSection}>
                            <div className={styles.formRow}>
                                <div className={styles.formGroup}>
                                    <label>Status Prospect *</label>
                                    <select required name="status" value={formData.status} onChange={handleChange}>
                                        {options.prospect_status?.map((o: any) => <option key={o.value} value={o.value}>{o.label}</option>)}
                                    </select>
                                </div>
                                <div className={styles.formGroup}>
                                    <label>Follow-up Berikutnya</label>
                                    <input type="date" name="next_followup_date" value={formData.next_followup_date || ''} onChange={handleChange} />
                                </div>
                            </div>
                            <div className={styles.formGroup}>
                                <label>Catatan Follow-up</label>
                                <textarea name="followup_notes" value={formData.followup_notes || ''} onChange={handleChange} rows={3}></textarea>
                            </div>
                        </div>
                    )}

                </form>

                <div className={styles.footer}>
                    <button type="button" className={styles.cancelButton} onClick={onClose}>Batal</button>
                    {activeTab > 0 && <button type="button" className={styles.cancelButton} onClick={() => setActiveTab(a => a - 1)}>Sebelumnya</button>}
                    {activeTab < tabs.length - 1 ? (
                        <button type="button" className={styles.submitButton} onClick={() => setActiveTab(a => a + 1)}>Selanjutnya</button>
                    ) : (
                        <button type="submit" form="prospectForm" className={styles.submitButton} disabled={loading}>
                            {loading ? 'Menyimpan...' : 'Simpan Calon Siswa'}
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
