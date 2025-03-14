import { useState, useCallback } from 'react';
import { json } from 'react-router-dom';
import Swal from 'sweetalert2';
import axios from 'axios';

// const apiUrl = process.env.REACT_APP_API_URL;
const apiUrl = 'http://localhost:8001';

const UseFetchWishlist = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    const [projects, setProjects] = useState(null);



    const fetchProjects = useCallback(async () => {
        setLoading(true);
        setError(null);
        setSuccess(false);

        try {
            const accessToken = localStorage.getItem('accessToken');

            // You don't need to include CSRF token for GET requests

            const response = await axios.get(`${apiUrl}/api/registration/wishlist/`, {
                // params: {
                //     accessToken: accessToken,
                // },
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`,
                },
            })


            if (response.status === 200) {
                setSuccess(true);
                console.log(response.data);
                setProjects(response.data);
            } else if (response.status === 400) {
                const jsonData = await response.data;
                setError(jsonData);
            }
            else if(response.status === 404){
                setError("404");
                console.log("404");
            }




        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    return { fetchProjects, setError, loading, error, success, projects, setProjects };
};

export default UseFetchWishlist;
