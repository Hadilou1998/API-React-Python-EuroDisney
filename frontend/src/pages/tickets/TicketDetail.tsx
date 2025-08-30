import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getTicket } from '../../api/endpoints';

export default function TicketDetail() {
    const { id } = useParams();
    const number = Number(id);
    const { data, isLoading } = useQuery({ queryKey: ['tickets', number], queryFn: () => getTicket(number), enabled: !!number });
    if (isLoading) return <p>Loading...</p>
    if (!data) return <p>Ticket not found</p>

    return (
        <div className="card">
            <h1>Ticket #{data.id}</h1>
            <p>User: {data.user_id}</p>
            <p>Attraction: {data.attraction_id}</p>
            <p>Date: {new Date(data.date).toLocaleString()}</p>
            <p>QR Code: {data.qr_code}</p>
        </div>
    );
};