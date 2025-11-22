import { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { deleteReservation, getReservation } from '../../api/endpoints';
import { useAuth } from '../../auth/AuthContext';
import type { Reservation } from '../../types/api';

export default function ReservationDetail() {
    const { id } = useParams();
    const { token, user } = useAuth();
    const nav = useNavigate();

    const [res, setRes] = useState<Reservation | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!token) return;
        getReservation(Number(id), token)
            .then(setRes)
            .finally(() => setLoading(false));
    }, [id, token]);

    if (loading) return <p>Loading...</p>;
    if (!res) return <p>Reservation not found</p>;

    const isAdmin = user?.role === "admin";
    const isEmployee = user?.role === "employee";
    const isOwner = user?.role === "user" && user.id === res.user_id;

    // User cannot view someone else's reservation
    if (user?.role === "user" && !isOwner) {
        return <p style={{ color: "crimson" }}>You are not allowed to see this reservation.</p>;
    }

    const canEdit = isAdmin || isOwner;

    const handleDelete = async () => {
        if (!window.confirm("Are you sure?")) return;
        await deleteReservation(res.id, token || "");
        nav('/reservations');
    };

    return (
        <div className="card" style={{ maxWidth: 600 }}>
            <h2>Reservation #{res.id}</h2>

            <p><b>User:</b> {res.user_id}</p>
            <p><b>Resource:</b> {res.resource_type}</p>
            <p><b>Date:</b> {new Date(res.date).toLocaleString()}</p>
            <p><b>Persons:</b> {res.nb_persons}</p>
            <p><b>Status:</b> {res.status}</p>
            {isEmployee && (
                <p style={{ marginTop: 10, color: "gray" }}>
                    Employees can view all reservations but cannot modify or delete them.
                </p>
            )}

            <div style={{ marginTop: 16 }}>
                <Link to="/reservations" className="btn">Back</Link>

                {canEdit && (
                    <>
                        <Link to={`/reservations/${res.id}/edit`} className="btn primary" style={{ marginLeft: 8 }}>
                            Edit
                        </Link>

                        <button className="btn danger" style={{ marginLeft: 8 }} onClick={handleDelete}>
                            Delete
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}