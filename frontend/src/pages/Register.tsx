import { useState } from 'react';
import { register } from '../api/endpoints';
import { useNavigate } from 'react-router-dom';
import FormField from '../components/FormField';

export default function Register() {
    const nav = useNavigate();
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [msg, setMsg] = useState<string | null>(null);

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setMsg(null);
        try {
            await register({ name, email, password });
            setMsg('Register success');
            setTimeout(() => nav('/login'), 800);
        } catch (err) {
            console.error(err);
            setMsg('Error while registering, please try again later');
        }
    };

    return (
        <form onSubmit={onSubmit} className="card" style={{ maxWidth: 480 }}>
            <h2>Inscription</h2>
            {msg && <p style={{ color: 'green' }}>{msg}</p>}
            <FormField label="Name">
                <input className="input" value={name} onChange={e => setName(e.target.value)} placeholder="Name" title="Enter your name" />
            </FormField>
            <FormField label="Email">
                <input className="input" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" title="Enter your email" />
            </FormField>
            <FormField label="Password">
                <input className="input" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" title="Enter your password" />
            </FormField>
            <button className="btn-primary">Register</button>
        </form>
    );
};