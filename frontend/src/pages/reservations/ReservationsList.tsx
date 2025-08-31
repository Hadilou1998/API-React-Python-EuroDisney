import { useQuery } from '@tanstack/react-query';
import { listReservations } from '../../api/endpoints';

export default function ReservationsList() {
    const { data, isLoading } = useQuery({ queryKey: ['reservations'], queryFn: listReservations });
    if (isLoading) return <p>Loading...</p>

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
                    {data?.map(res => (
                        <tr key={res.id}>
                            <td>{res.user_id}</td>
                            <td>{res.resource_type}</td>
                            <td>{new Date(res.date).toLocaleString()}</td>
                            <td>{res.nb_persons}</td>
                            <td>{res.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    );
};