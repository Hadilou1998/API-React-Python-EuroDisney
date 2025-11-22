import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createAttraction, getAttraction, updateAttraction } from '../../api/endpoints';
import FormField from '../../components/FormField';
import { useAuth } from '../../auth/AuthContext';

export default function AttractionForm() {
    const { id } = useParams();
    const editing = Boolean(id);
    const nav = useNavigate();
    const { token } = useAuth();
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [capacity, setCapacity] = useState(0);
    const [status, setStatus] = useState<'open' | 'closed' | 'maintenance'>('open');

    useEffect(() => {
        if (editing && token) {
            getAttraction(Number(id)).then(a => {
                setName(a.name);
                setDescription(a.description);
                setCapacity(a.capacity);
                setStatus(a.status);
            });
        }
    }, [editing, id, token]);

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        
        if (!token) {
            alert("No token found — please login!");
            return;
        }

        if (editing) {
            await updateAttraction(
                Number(id),
                { name, description, capacity, status },
                token
            );
        } else {
            await createAttraction(
                { name, description, capacity, status },
                token
            );
        }

        nav('/attractions');
    };

    return (
        <form className="card" onSubmit={onSubmit} style={{ maxWidth: 640 }}>
            <h2>{editing ? 'Update' : 'Create'} an attraction</h2>
            <FormField label="Name">
                <input className="input" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" title="Name of the attraction" />
            </FormField>
            <FormField label="Description">
                <input className="input" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" title="Description of the attraction" />
            </FormField>
            <FormField label="Capacity">
                <input type="number" className="input" value={capacity} onChange={(e) => setCapacity(Number(e.target.value))} placeholder="Capacity" title="Capacity of the attraction" min={0} />
            </FormField>
            <FormField label="Status">
                <select className="input" value={status} onChange={(e) => setStatus(e.target.value as 'open' | 'closed' | 'maintenance')} title="Status of the attraction">
                    <option value="open">Open</option>
                    <option value="closed">Closed</option>
                    <option value="maintenance">Maintenance</option>
                </select>
            </FormField>
            <button className="btn primary">{editing ? 'Update' : 'Create'}</button>
        </form>
    );
};