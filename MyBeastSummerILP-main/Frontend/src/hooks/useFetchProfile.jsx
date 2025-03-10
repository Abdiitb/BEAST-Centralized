import { useState, useCallback, useEffect } from 'react';
import axios from 'axios';

// const apiUrl = process.env.REACT_APP_API_URL;
const apiUrl = 'http://localhost:8001';

const UseFetchProfile = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    const [fetchedProfile, setFetchedProfile] = useState(null);

    const fetchProfile = useCallback(async () => {
        setLoading(true);
        setError(null);
        setSuccess(false);

        try {
            const accessToken = localStorage.getItem('accessToken');

            const response = await axios.get(`${apiUrl}/api/authentication/profile/`, {
                // params: {
                //     accessToken: accessToken,
                // },
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`,
                },
            });

            if (response.status === 200) {
                setSuccess(true);
                setFetchedProfile(response.data);
                console.log(fetchedProfile);
            } else if (response.status === 400 || response.status === 404) {
                setError(response.data);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        if (fetchedProfile !== null) {
            console.log(fetchedProfile);
        }
    }, [fetchedProfile]);

    return { fetchProfile, setError, loading, error, success, fetchedProfile };
};

export default UseFetchProfile;
