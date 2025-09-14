import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { listTickets } from '../../api/endpoints';
import { useAuth } from '../../auth/AuthContext';

export default function TicketsList() {
    const { token } = useAuth();

    const { data, isLoading, error } = useQuery({ 
        queryKey: ['tickets'], 
        queryFn: () => listTickets(token || ""),
        enabled: !!token,
    });
    
    if (isLoading) return <p>Loading...</p>
    if (error) return <p>Error: {error.message}</p>

    // Protection if data is not a array
    const tickets = Array.isArray(data) ? data : [];

    return (
        <>
            <h2>Tickets</h2>
            <table className="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>User</th>
                        <th>Attraction</th>
                        <th>Date</th>
                        <th>QR_CODE</th>
                    </tr>
                </thead>
                <tbody>
                    {tickets.length > 0 ? (
                        tickets.map(t => (
                            <tr key={t.id}>
                                <td><Link to={`/${t.id}`}>{t.id}</Link></td>
                                <td>{t.user_id}</td>
                                <td>{t.attraction_id}</td>
                                <td>{new Date(t.date).toLocaleString()}</td>
                                <td>{t.qr_code}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan={5}>No tickets available</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </>
    );
};