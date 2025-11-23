import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createReservation, getReservation, updateReservation } from '../../api/endpoints';
import { useAuth } from '../../auth/AuthContext';

export default function ReservationForm() {
    const { id } = useParams();
    const editing = Boolean(id);
    const nav = useNavigate();
    const { token, user } = useAuth();

    const [resource, setResource] = useState('');
    const [date, setDate] = useState('');
    const [persons, setPersons] = useState(1);
    const [status, setStatus] = useState<'pending' | 'confirmed' | 'cancelled'>('pending');

    useEffect(() => {
        if (editing && token) {
            getReservation(Number(id), token).then(r => {
                setResource(r.resource_type);
                setDate(r.date.slice(0, 16));
                setPersons(r.nb_persons);
                setStatus(r.status);
            });
        }
    }, [editing, id, token]);

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!token) return alert("Login required");

        const payload = {
            resource_type: resource,
            date,
            nb_persons: persons,
            user_id: user?.id,
            status,
        };

        if (editing) {
            await updateReservation(Number(id), payload, token);
        } else {
            await createReservation(payload, token);
        }

        nav('/reservations');
    };

    return (
        <form className="card" onSubmit={onSubmit} style={{ maxWidth: 640 }}>
            <h2>{editing ? 'Update' : 'Create'} Reservation</h2>

            <label htmlFor="resField">Resource</label>
            <input
                id="resField"
                className="input"
                value={resource}
                onChange={e => setResource(e.target.value)}
                placeholder="Restaurant, show, event..."
                title="Name of the place you want to reserve"
                required
            />

            <label htmlFor="dateField" style={{ marginTop: 8 }}>Date</label>
            <input
                id="dateField"
                type="datetime-local"
                className="input"
                value={date}
                onChange={e => setDate(e.target.value)}
                required
                title="Choose the reservation date and time"
                placeholder="Select date and time"
            />

            <label htmlFor="personsField" style={{ marginTop: 8 }}>Persons</label>
            <input
                id="personsField"
                type="number"
                className="input"
                min={1}
                value={persons}
                placeholder="Number of persons"
                title="Enter how many people"
                onChange={e => setPersons(Number(e.target.value))}
                required
            />

            {editing && user?.role === "admin" && (
                <>
                    <label htmlFor="statusField" style={{ marginTop: 8 }}>Status</label>
                    <select
                        id="statusField"
                        className="input"
                        value={status}
                        onChange={e => setStatus(e.target.value as 'pending' | 'confirmed' | 'cancelled')}
                    >
                        <option value="pending">Pending</option>
                        <option value="confirmed">Confirmed</option>
                        <option value="cancelled">Cancelled</option>
                    </select>
                </>
            )}

            <button className="btn primary" style={{ marginTop: 12 }}>
                {editing ? 'Update' : 'Create'}
            </button>
        </form>
    );
}