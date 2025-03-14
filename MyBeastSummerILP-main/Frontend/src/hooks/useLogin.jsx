import { useState, useCallback } from 'react';
import { json } from 'react-router-dom';
import Swal from 'sweetalert2';

// const apiUrl = process.env.REACT_APP_API_URL;
const apiUrl = 'http://localhost:8001';

const UseLogin = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const Login = useCallback(async (userData) => {
        setLoading(true);
        setError(null);
        setSuccess(false);

        try {
            // Get CSRF token from cookies
            const csrfTokenMatch = document.cookie.match(/csrftoken=([^;]+)/);
            const csrfToken = csrfTokenMatch ? csrfTokenMatch[1] : 'DUMMY_CSRF_TOKEN';
            const response = await fetch(`${apiUrl}/api/authentication/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Include CSRF token in headers
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(userData),
            });
            console.log(response);
            if (response.status === 200) {
                setSuccess(true);
                const jsonData = await response.json();
                localStorage.setItem('accessToken', jsonData['accessToken']);
                localStorage.setItem('refreshToken', jsonData['refreshToken']);
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 2000,
                    timerProgressBar: true,
                })
                Toast.fire({
                    icon: 'success',
                    title: 'Successfully Signed in'
                })
            }
            if (response.status === 400) {
                const jsonData = await response.json();
                setError(jsonData['error']);
            }
            if (response.status === 401) {
                const jsonData = await response.json();
                setError(jsonData['error']);
            }

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    return { Login, setError, loading, error, success };
};

export default UseLogin;
