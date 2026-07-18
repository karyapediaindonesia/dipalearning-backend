const API_URL = 'http://localhost:8000/api';

const getHeaders = () => {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
};

export const getBranches = async () => {
    const response = await fetch(`${API_URL}/branches/`, {
        headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch branches');
    return response.json();
};

export const createBranch = async (data: any) => {
    const response = await fetch(`${API_URL}/branches/`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to create branch');
    return response.json();
};

export const updateBranch = async (id: string, data: any) => {
    const response = await fetch(`${API_URL}/branches/${id}/`, {
        method: 'PUT',
        headers: getHeaders(),
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to update branch');
    return response.json();
};

export const deleteBranch = async (id: string) => {
    const response = await fetch(`${API_URL}/branches/${id}/`, {
        method: 'DELETE',
        headers: getHeaders()
    });
    if (!response.ok) {
        try {
            const data = await response.json();
            if (data?.error?.message) {
                throw new Error(data.error.message);
            }
        } catch (e: any) {
            if (e.message && e.message !== 'Failed to parse JSON') {
                throw e;
            }
        }
        throw new Error('Gagal menghapus cabang.');
    }
};
