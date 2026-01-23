import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';

interface ProtectedRouteProps {
    children: React.ReactElement;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    const { isLoggedIn, isLoading } = useAuth();

    if (isLoading) {
        return <div>Ładowanie...</div>; // Można tu dać ładny spinner
    }

    if (!isLoggedIn) {
        return <Navigate to="/logowanie" replace />;
    }

    return children;
};

export default ProtectedRoute;
