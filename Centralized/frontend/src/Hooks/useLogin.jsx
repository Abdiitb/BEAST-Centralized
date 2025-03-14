import { useState, useCallback, useContext } from 'react';
import Swal from 'sweetalert2';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { AuthContext } from '../Contexts/AuthContext';

// const apiUrl = process.env.REACT_APP_API_URL;
// console.log(apiUrl);  // It will print: http://localhost:8000/api

const UseLogin = () => {
    const { setLoggedIn } = useContext(AuthContext);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate(); // Initialize useNavigate

    const Login = useCallback(async (userData) => {
        setLoading(true);
        setError(null);
        setSuccess(false);

        try {
            // Get CSRF token from cookies
            const csrfTokenMatch = document.cookie.match(/csrftoken=([^;]+)/);
            const csrfToken = csrfTokenMatch ? csrfTokenMatch[1] : 'DUMMY_CSRF_TOKEN';
            // const response = await fetch(`${apiUrl}/api/authentication/login/`, {
            const response = await fetch(`http://localhost:8000/api/authentication/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Include CSRF token in headers
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(userData),
            });

            if (response.status === 200) {
                setSuccess(true);
                const jsonData = await response.json();
                localStorage.setItem('accessToken', jsonData['access']);
                localStorage.setItem('refreshToken', jsonData['refresh']);
                setLoggedIn(true);
                Swal.fire({
                    icon: 'success',
                    title: 'Successfully Logged In',
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 2000,
                    timerProgressBar: true,
                }).then(() => {
                    navigate('/'); // Redirect to home page after successful login
                });
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
    }, [navigate, setLoggedIn]);

    return { Login, setError, loading, error, success };
};

export default UseLogin;
