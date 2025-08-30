import { useAuth } from '../auth/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { listAttractions, listTickets, listEmployees, listReservations } from '../api/endpoints';

export default function Dashboard() {
    const { user } = useAuth();
    const { data: attractions } = useQuery({ queryKey:['attractions'], queryFn: listAttractions });
    const { data: tickets } = useQuery({ queryKey:['tickets'], queryFn: listTickets });
    const { data: employees } = useQuery({ queryKey:['employees'], queryFn: listEmployees });
    const { data: reservations } = useQuery({ queryKey:['reservations'], queryFn: listReservations });

    return (
        <div>
            <h2>Tableau de bord</h2>
            <p>Bonjour, {user?.name}</p>
            <div className="card">
                <strong>Stats rapides</strong>
                <ul>
                    <li>Attractions: {attractions?.length ?? 0}</li>
                    <li>Tickets: {tickets?.length ?? 0}</li>
                    <li>Employees: {employees?.length ?? 0}</li>
                    <li>Reservations: {reservations?.length ?? 0}</li>
                </ul>
            </div>
        </div>
    );
};