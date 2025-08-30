import { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { LoginPayload, LoginResponse, User } from "../types/api";
import { login } from "../api/endpoints";

type AuthCtx = {
    user: User | null;
    token: string | null;
    loginFn: (p: LoginPayload) => Promise<void>;
    logout: () => void;
}

const Ctx = createContext<AuthCtx | null>(null)
// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
    const ctx = useContext(Ctx)
    if (!ctx) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return ctx
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);

    useEffect(() => {
        const token = localStorage.getItem('test');
        const user = localStorage.getItem('user');
        if (token) {
            setToken(token);
        }
        if (user) {
            setUser(JSON.parse(user));
        }        
    }, [])

    const loginFn = async (p: LoginPayload) => {
        const res: LoginResponse = await login(p)
        localStorage.setItem('test', res.access_token);
        localStorage.setItem('user', JSON.stringify(res.user));
        setToken(res.access_token);
        setUser(res.user);
    }
    
    const logout = () => {
        localStorage.removeItem('test');
        localStorage.removeItem('user');
        setToken(null);
        setUser(null);
    }

    const value = useMemo(() => ({ user, token, loginFn, logout }), [user, token]);

    return (
        <Ctx.Provider value={value}>{children}</Ctx.Provider>
    );
}