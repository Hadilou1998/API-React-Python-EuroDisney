import { useQuery } from '@tanstack/react-query';
import { listReservations } from '../../api/endpoints';

export default function ReservationsList() {
    const { data, isLoading } = useQuery({ queryKey: ['reservations'], queryFn: listReservations });
    if (isLoading) return <p>Loading...</p>

    // Protection if data is not a array
    const reservations = Array.isArray(data) ? data : [];

    return (
        <>
            <h2>Reservations</h2>
            <table className="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>User</th>
                        <th>Resource</th>
                        <th>Date</th>
                        <th>Persons</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {reservations.length > 0 ? (
                        reservations.map(res => (
                            <tr key={res.id}>
                                <td>{res.user_id}</td>
                                <td>{res.resource_type}</td>
                                <td>{new Date(res.date).toLocaleString()}</td>
                                <td>{res.nb_persons}</td>
                                <td>{res.status}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan={6}>No reservations available</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </>
    );
};