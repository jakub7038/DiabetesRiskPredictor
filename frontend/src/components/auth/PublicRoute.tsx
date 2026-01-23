import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';

interface PublicRouteProps {
    children: React.ReactElement;
}

const PublicRoute = ({ children }: PublicRouteProps) => {
    const { isLoggedIn, isLoading } = useAuth();

    if (isLoading) {
        return <div>Ładowanie...</div>;
    }

    if (isLoggedIn) {
        return <Navigate to="/konto" replace />;
    }

    return children;
};

export default PublicRoute;
