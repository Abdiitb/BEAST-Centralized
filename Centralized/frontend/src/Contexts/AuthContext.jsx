import { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('accessToken'));

    useEffect(() => {
        const checkAuth = () => {
            setLoggedIn(!!localStorage.getItem('accessToken'));
        };

        window.addEventListener('storage', checkAuth); // Listen for storage changes
        return () => window.removeEventListener('storage', checkAuth);
    }, []);

    return (
        <AuthContext.Provider value={{ loggedIn, setLoggedIn }}>
            {children}
        </AuthContext.Provider>
    );
};
