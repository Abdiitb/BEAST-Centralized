import { useState, useCallback } from 'react';
import Swal from 'sweetalert2';

// const apiUrl = process.env.REACT_APP_API_URL;
const UseSignup = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const signup = useCallback(async (userData) => {
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Get CSRF token from cookies
      const csrfTokenMatch = document.cookie.match(/csrftoken=([^;]+)/);
      const csrfToken = csrfTokenMatch ? csrfTokenMatch[1] : 'DUMMY_CSRF_TOKEN';

      const response = await fetch(`http://localhost:8000/api/authentication/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Include CSRF token in headers
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(userData),
      });

      if(response.status === 201){
        setSuccess(true);
        Swal.fire({
            icon: 'success',
            title: 'Success!',
            text: 'Verification link has been sent to your webmail. Please verify your account to login.',
            confirmButtonText: 'OK',
          }).then((result) => {
            if (result.isConfirmed) {
              window.location.href = '/login';
            }
          });
      }
      if(response.status === 400){
        setError("User already exists, please login");
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { signup, loading, error, success };
};

export default UseSignup;
