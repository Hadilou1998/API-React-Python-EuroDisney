import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createTicket, getTicket, updateTicket } from '../../api/endpoints';
import { useAuth } from '../../auth/AuthContext';

export default function TicketForm() {
    const { id } = useParams();
    const editing = Boolean(id);
    const nav = useNavigate();
    const { token, user } = useAuth();

    // Hooks ALWAYS first
    const [userId, setUserId] = useState(0);
    const [attractionId, setAttractionId] = useState(0);
    const [date, setDate] = useState('');
    const [qrCode, setQrCode] = useState('');

    useEffect(() => {
        if (editing && token) {
            getTicket(Number(id), token).then(t => {
                setUserId(t.user_id);
                setAttractionId(t.attraction_id);
                setDate(t.date.slice(0, 16));
                setQrCode(t.qr_code);
            });
        }
    }, [editing, id, token]);

    // Only admin allowed
    if (user?.role !== "admin") {
        return <p style={{ color: "crimson" }}>Only admin can manage tickets.</p>;
    }

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!token) return alert("Login required");

        const payload = {
            user_id: userId,
            attraction_id: attractionId,
            date,
            qr_code: qrCode,
        };

        if (editing) {
            await updateTicket(Number(id), payload, token);
        } else {
            await createTicket(payload, token);
        }

        nav('/tickets');
    };

    return (
        <form className="card" onSubmit={onSubmit} style={{ maxWidth: 640 }}>
            <h2>{editing ? 'Update' : 'Create'} Ticket</h2>

            <label htmlFor="userIdField">User ID</label>
            <input
                id="userIdField"
                className="input"
                type="number"
                value={userId}
                placeholder="Enter user ID"
                title="Enter the ID of the user"
                onChange={e => setUserId(Number(e.target.value))}
            />

            <label htmlFor="attractionIdField" style={{ marginTop: 8 }}>Attraction ID</label>
            <input
                id="attractionIdField"
                className="input"
                type="number"
                value={attractionId}
                placeholder="Enter attraction ID"
                title="Enter the ID of the attraction"
                onChange={e => setAttractionId(Number(e.target.value))}
            />

            <label htmlFor="dateField" style={{ marginTop: 8 }}>Date</label>
            <input
                id="dateField"
                type="datetime-local"
                className="input"
                value={date}
                placeholder="Select date and time"
                title="Choose the ticket date and time"
                onChange={e => setDate(e.target.value)}
            />

            <label htmlFor="qrField" style={{ marginTop: 8 }}>QR Code</label>
            <input
                id="qrField"
                className="input"
                value={qrCode}
                placeholder="Enter QR code"
                title="Enter the QR code of the ticket"
                onChange={e => setQrCode(e.target.value)}
            />

            <button className="btn primary" style={{ marginTop: 12 }}>
                {editing ? 'Update' : 'Create'}
            </button>
        </form>
    );
}