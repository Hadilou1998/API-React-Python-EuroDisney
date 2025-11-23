import { createContext, useContext, useEffect, useMemo, useState, useCallback } from "react";
import type { LoginPayload, LoginResponse, User } from "../types/api";
import { login } from "../api/endpoints";

type AuthCtx = {
    user: User | null;
    token: string | null;
    loginFn: (p: LoginPayload) => Promise<LoginResponse>;
    logout: () => void;
};

const Ctx = createContext<AuthCtx | null>(null);

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
    const ctx = useContext(Ctx);
    if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
    return ctx;
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);

    // Decode JWT inline to avoid extra exports (fix react-refresh)
    const decodeJWT = useCallback((token: string) => {
        try {
            const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
            return JSON.parse(atob(base64));
        } catch {
            return null;
        }
    }, []);

    // Load stored token/user
    useEffect(() => {
        const storedToken = localStorage.getItem("test");

        if (storedToken) {
            setToken(storedToken);
            const payload = decodeJWT(storedToken);

            if (payload) {
                const rebuiltUser: User = {
                    id: Number(payload.sub),
                    name: payload.name ?? "",
                    email: payload.email ?? "",
                    role: payload.role,
                };

                setUser(rebuiltUser);
                localStorage.setItem("user", JSON.stringify(rebuiltUser));
            }
        }
    }, [decodeJWT]);

    // -------- FIX: wrap loginFn in useCallback --------
    const loginFn = useCallback(async (p: LoginPayload) => {
        const res: LoginResponse & { user: User } = await login(p);

        localStorage.setItem("test", res.access_token);
        setToken(res.access_token);

        const payload = decodeJWT(res.access_token);
        if (!payload) throw new Error("Invalid JWT token");

        const newUser: User = {
            id: Number(payload.sub),
            name: payload.name ?? res.user.name ?? "",
            email: payload.email ?? res.user.email ?? "",
            role: payload.role,
        };

        setUser(newUser);
        localStorage.setItem("user", JSON.stringify(newUser));

        return res;
    }, [decodeJWT]);

    // -------- FIX: wrap logout in useCallback --------
    const logout = useCallback(() => {
        localStorage.removeItem("test");
        localStorage.removeItem("user");
        setToken(null);
        setUser(null);
    }, []);

    // -------- FIX ESLint exhaustive-deps --------
    const value = useMemo(
        () => ({ user, token, loginFn, logout }),
        [user, token, loginFn, logout]
    );

    return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}