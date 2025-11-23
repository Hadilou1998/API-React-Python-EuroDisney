import { useEffect, useState, useCallback } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { deleteReservation, getReservation } from '../../api/endpoints';
import { useAuth } from '../../auth/AuthContext';
import type { Reservation } from '../../types/api';

export default function ReservationDetail() {
    const { id } = useParams();
    const nav = useNavigate();
    const { token, user } = useAuth();

    const [res, setRes] = useState<Reservation | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // -----------------------------
    // Fetch reservation (stable)
    // -----------------------------
    const fetchReservation = useCallback(async () => {
        if (!token || !id) return; // NE PAS appeler l’API sans token

        try {
            const data = await getReservation(Number(id), token);
            setRes(data);
            setError(null);
        } catch (err) {
            console.error("Error loading reservation:", err);
            setError("forbidden_or_not_found");
            setRes(null);
        } finally {
            setLoading(false);
        }
    }, [id, token]);

    // -----------------------------
    // Load on mount
    // -----------------------------
    useEffect(() => {
        if (token) fetchReservation(); // attends que le token soit chargé
    }, [fetchReservation, token]);

    // -----------------------------
    // Render logic
    // -----------------------------
    if (!token) return <p>You must be logged in.</p>;
    if (loading) return <p>Loading...</p>;

    if (error === "forbidden_or_not_found")
        return <p style={{ color: "crimson" }}>Reservation not found or access denied.</p>;

    if (!res)
        return <p>Unable to load reservation.</p>;

    const isAdmin = user?.role === "admin";
    const isEmployee = user?.role === "employee";
    const isOwner = user?.role === "user" && user.id === res.user_id;

    if (user?.role === "user" && !isOwner)
        return <p style={{ color: "crimson" }}>You are not allowed to see this reservation.</p>;

    const canEdit = isAdmin || isOwner;

    // -----------------------------
    // Delete handler
    // -----------------------------
    const handleDelete = async () => {
        if (!window.confirm("Are you sure?")) return;
        await deleteReservation(res.id, token);
        nav('/reservations');
    };

    // -----------------------------
    // Render component
    // -----------------------------
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
                    Employees can view reservations but cannot modify or delete them.
                </p>
            )}

            <div style={{ marginTop: 16 }}>
                <Link to="/reservations" className="btn">Back</Link>

                {canEdit && (
                    <>
                        <Link
                            to={`/reservations/${res.id}/edit`}
                            className="btn primary"
                            style={{ marginLeft: 8 }}
                        >
                            Edit
                        </Link>

                        <button
                            className="btn danger"
                            style={{ marginLeft: 8 }}
                            onClick={handleDelete}
                        >
                            Delete
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}