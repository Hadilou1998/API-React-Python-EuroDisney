import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { listTickets } from '../../api/endpoints';
import { useAuth } from '../../auth/AuthContext';

export default function TicketsList() {
    const { token, user } = useAuth();

    const { data, isLoading, error } = useQuery({ 
        queryKey: ['tickets'], 
        queryFn: () => listTickets(token || ""),
        enabled: !!token,
    });
    
    if (isLoading) return <p>Loading...</p>
    if (error) return <p>Error: {error.message}</p>

    // Protection if data is not a array
    const tickets = Array.isArray(data) ? data : [];

    const canManage = user?.role === "admin";
    const filtered = user?.role === "user"
        ? tickets.filter(t => t.user_id === user.id)
        : tickets;

    return (
        <>
            <h2>Tickets</h2>
            {canManage && (
                <Link className="btn primary" to="/tickets/new">Create Ticket</Link>
            )}
            <table className="table" style={{ marginTop: 16 }}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>User</th>
                        <th>Attraction</th>
                        <th>Date</th>
                        <th>QR_CODE</th>
                        {canManage && <th>Actions</th>}
                    </tr>
                </thead>
                <tbody>
                    {filtered.length > 0 ? filtered.map(t => (
                        <tr key={t.id}>
                            <td>{t.id}</td>
                            <td>{t.user_id}</td>
                            <td>{t.attraction_id}</td>
                            <td>{new Date(t.date).toLocaleString()}</td>
                            <td>{t.qr_code}</td>
                            {canManage && (
                                <td>
                                    <Link to={`/tickets/${t.id}/edit`} className="btn small">Edit</Link>
                                </td>
                            )}
                        </tr>
                    )) : (
                        <tr>
                            <td colSpan={5}>No tickets available</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </>
    );
};