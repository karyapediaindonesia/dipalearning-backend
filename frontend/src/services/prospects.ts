const API_URL = 'http://localhost:8000/api/v1';

const getHeaders = () => {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
};

export const getProspects = async () => {
    const response = await fetch(`${API_URL}/students/prospects/`, {
        headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch prospects');
    return response.json();
};

export const getProspectOptions = async () => {
    const response = await fetch(`${API_URL}/students/prospects/options/`, {
        headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch prospect options');
    return response.json();
};

export const createProspect = async (data: any) => {
    const response = await fetch(`${API_URL}/students/prospects/`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to create prospect');
    return response.json();
};

export const updateProspect = async (id: string, data: any) => {
    const response = await fetch(`${API_URL}/students/prospects/${id}/`, {
        method: 'PUT',
        headers: getHeaders(),
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to update prospect');
    return response.json();
};

export const deleteProspect = async (id: string) => {
    const response = await fetch(`${API_URL}/students/prospects/${id}/`, {
        method: 'DELETE',
        headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to delete prospect');
};
