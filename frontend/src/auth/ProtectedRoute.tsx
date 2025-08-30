import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import type { JSX } from "react/jsx-runtime";

export default function ProtectedRoute({ children, roles }: { children: JSX.Element, roles?: Array< 'user' | 'employee' | 'admin' > }) {
    const { user } = useAuth();
    if (!user) return <Navigate to="/login" replace />;
    if (roles && !roles.includes(user.role)) return <Navigate to="/unauthorized" replace />;
    return children;
};