import { useQuery } from '@tanstack/react-query';
import { listReservations } from '../../api/endpoints';
import { useAuth } from '../../auth/AuthContext';
import { Link } from 'react-router-dom';

export default function ReservationsList() {
    const { token, user } = useAuth();

    const { data, isLoading, error } = useQuery({
        queryKey: ['reservations'],
        queryFn: () => listReservations(token || ""),
        enabled: !!token,
    });

    if (!token) return <p>You must be logged in.</p>;
    if (isLoading) return <p>Loading...</p>;
    if (error) return <p>Error loading reservations.</p>;

    const reservations = Array.isArray(data) ? data : [];

    const isUser = user?.role === "user";
    const isEmployee = user?.role === "employee";
    const isAdmin = user?.role === "admin";

    // Filtrer pour utilisateur
    const filteredReservations =
        isUser 
            ? reservations.filter(r => Number(r.user_id) === Number(user.id)) 
            : reservations;

    return (
        <>
            <h2>Reservations</h2>

            {isEmployee && (
                <p style={{ color: "gray", marginBottom: 12 }}>
                    Employees can view all reservations but cannot modify or delete them.
                </p>
            )}

            {isUser && (
                <Link className="btn primary" to="/reservations/new" style={{ marginBottom: 12 }}>
                    Create a reservation
                </Link>
            )}

            <table className="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>User</th>
                        <th>Resource</th>
                        <th>Date</th>
                        <th>Persons</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>
                    {filteredReservations.length > 0 ? (
                        filteredReservations.map(res => {
                            const isOwner = isUser && res.user_id === user.id;
                            const canEdit = isAdmin || isOwner;

                            return (
                                <tr key={res.id}>
                                    <td>{res.id}</td>
                                    <td>{res.user_id}</td>
                                    <td>{res.resource_type}</td>
                                    <td>{new Date(res.date).toLocaleString()}</td>
                                    <td>{res.nb_persons}</td>
                                    <td>{res.status}</td>

                                    <td>
                                        <Link className="btn small" to={`/reservations/${res.id}`}>
                                            View
                                        </Link>

                                        {canEdit && (
                                            <Link
                                                className="btn small primary"
                                                style={{ marginLeft: 6 }}
                                                to={`/reservations/${res.id}/edit`}
                                            >
                                                Edit
                                            </Link>
                                        )}
                                    </td>
                                </tr>
                            );
                        })
                    ) : (
                        <tr>
                            <td colSpan={7}>No reservations found</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </>
    );
}