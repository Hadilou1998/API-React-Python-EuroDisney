import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { listTickets } from '../../api/endpoints';

export default function TicketsList() {
    const { data, isLoading } = useQuery({ queryKey: ['tickets'], queryFn: listTickets });
    if (isLoading) return <p>Loading...</p>

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
                    {data?.map((t) => (
                        <tr key={t.id}>
                            <td><Link to={`/tickets/${t.id}`}>{t.id}</Link></td>
                            <td>{t.user_id}</td>
                            <td>{t.attraction_id}</td>
                            <td>{new Date(t.date).toLocaleString()}</td>
                            <td>{t.qr_code}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    );
};