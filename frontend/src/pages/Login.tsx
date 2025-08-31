/* webhint-disable no-inline-styles */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import FormField from '../components/FormField';

export default function Login() {
    const { loginFn } = useAuth();
    const nav = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            const res = await loginFn({ email, password });

            console.log("=== Login Success ===");
            console.log("Token:", res.access_token);
            console.log("User:", res.user);

            // Affichage message et redirection
            alert(`Welcome ${res.user.name}! You are now logged in.`);
            nav('/dashboard'); // redirection vers la page d’accueil / dashboard

            // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (err: any) {
            console.error("Login failed:", err);
            setError(err?.message || 'Connection failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={onSubmit} className="card" style={{ maxWidth: 420 }}>
            <h2>Connexion</h2>
            {error && <p style={{ color: 'crimson' }}>{error}</p>}
            <FormField label="Email">
                <input className="input" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" title="Enter your email" />
            </FormField>
            <FormField label="Password">
                <input className="input" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" title="Enter your password" />
            </FormField>
            <button className="btn-primary" disabled={loading}>{loading ? 'Loading...' : 'Login'}</button>
        </form>
    );
};