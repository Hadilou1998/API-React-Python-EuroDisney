import { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { LoginPayload, LoginResponse, User } from "../types/api";
import { login } from "../api/endpoints";

type AuthCtx = {
    user: User | null;
    token: string | null;
    loginFn: (p: LoginPayload) => Promise<LoginResponse & { user: User }>;
    logout: () => void;
};

const Ctx = createContext<AuthCtx | null>(null);

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
    const ctx = useContext(Ctx);
    if (!ctx) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return ctx;
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);

    // Charger les données depuis localStorage au démarrage
    useEffect(() => {
        const storedToken = localStorage.getItem("test");
        const storedUser = localStorage.getItem("user");

        if (storedToken) setToken(storedToken);
        if (storedUser) {
            try {
                const parsedUser = JSON.parse(storedUser);
                setUser(parsedUser);
            } catch (e) {
                console.warn("Failed to parse stored user:", e);
                localStorage.removeItem("user");
            }
        }
    }, []);

    // Fonction de login
    const loginFn = async (p: LoginPayload): Promise<LoginResponse & { user: User }> => {
        const res: LoginResponse & { user: User } = await login(p);

        // stock token
        localStorage.setItem("test", res.access_token);
        setToken(res.access_token);

        // stock user
        localStorage.setItem("user", JSON.stringify(res.user));
        setUser(res.user);

        return res;
    };

    // Fonction de logout
    const logout = () => {
        localStorage.removeItem("test");
        localStorage.removeItem("user");
        setToken(null);
        setUser(null);
    };

    // Valeur du contexte
    const value = useMemo(() => ({ user, token, loginFn, logout }), [user, token]);

    return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}