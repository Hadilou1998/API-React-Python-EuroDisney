import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';

export default function Login() {
    const { login } = useAuth();
    const nav = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            await login({ email, password });
            nav('/dashboard');
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (e: any) {
            setError(e?.response?.data?.detail ?? 'Connection failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={onSubmit}>
            <h2>Connexion</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <label htmlFor='email'>Email</label>
            <input id='email' className='input' value={email} onChange={e => setEmail(e.target.value)} required />
            <label htmlFor='password' style={{ marginTop: '1rem' }}>Mot de passe</label>
            <input id='password' className='input' type="password" value={password} onChange={e => setPassword(e.target.value)} required />
            <div style={{ marginTop: '1rem' }}>
                <button className='btn primary' disabled={loading}>{loading ? 'Chargement...' : 'Se connecter'}</button>
            </div>
        </form>
    );
};