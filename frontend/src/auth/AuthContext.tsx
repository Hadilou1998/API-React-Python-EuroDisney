import { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { LoginPayload, LoginResponse, User } from "../types/api";
import { login } from "../api/endpoints";

type AuthCtx = {
    user: User | null;
    token: string | null;
    loginFn: (p: LoginPayload) => Promise<void>;
    logout: () => void;
};

const Ctx = createContext<AuthCtx | null>(null);

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
    const ctx = useContext(Ctx);
    if (!ctx) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return ctx;
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);

    useEffect(() => {
        const storedToken = localStorage.getItem('test');
        const storedUser = localStorage.getItem('user');

        if (storedToken) {
            setToken(storedToken);
        }

        if (storedUser) {
            try {
                setUser(JSON.parse(storedUser));
            } catch (err) {
                console.warn("Failed to parse stored user:", err);
                setUser(null);
            }
        }
    }, []);

    const loginFn = async (p: LoginPayload) => {
        try {
            const res: LoginResponse = await login(p);
            localStorage.setItem('test', res.access_token);
            localStorage.setItem('user', JSON.stringify(res.user));
            setToken(res.access_token);
            setUser(res.user);
        } catch (err) {
            console.error("Login failed:", err);
            throw err;
        }
    };
    
    const logout = () => {
        localStorage.removeItem('test');
        localStorage.removeItem('user');
        setToken(null);
        setUser(null);
    };

    const value = useMemo(() => ({ user, token, loginFn, logout }), [user, token]);

    return (
        <Ctx.Provider value={value}>
            {children}
        </Ctx.Provider>
    );
};