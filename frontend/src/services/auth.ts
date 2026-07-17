export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const login = async (username: string, password: string) => {
    const response = await fetch(`${API_URL}/auth/login/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
        throw new Error(data.non_field_errors?.[0] || data.detail || 'Login failed');
    }
    
    if (data.access) {
        sessionStorage.setItem('access_token', data.access);
        sessionStorage.setItem('refresh_token', data.refresh);
        sessionStorage.setItem('user', JSON.stringify(data.user));
        // Also set as cookie for Next.js middleware to read
        document.cookie = `access_token=${data.access}; path=/; max-age=86400`; // 1 day
    }
    
    return data;
};

export const logout = () => {
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('refresh_token');
    sessionStorage.removeItem('user');
    // Remove cookie
    document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
};

export const getMe = async () => {
    const token = sessionStorage.getItem('access_token');
    if (!token) throw new Error('No token found');

    const response = await fetch(`${API_URL}/auth/me/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        throw new Error('Failed to fetch user');
    }

    return await response.json();
};

export const updateMe = async (formData: FormData) => {
    const token = sessionStorage.getItem('access_token');
    if (!token) throw new Error('No token found');

    const response = await fetch(`${API_URL}/auth/me/`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${token}`,
            // Do not set Content-Type, the browser will set it to multipart/form-data with boundary
        },
        body: formData,
    });

    if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to update user');
    }

    const data = await response.json();
    sessionStorage.setItem('user', JSON.stringify(data));
    return data;
};
