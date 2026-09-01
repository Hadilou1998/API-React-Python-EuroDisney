import { useAuth } from '../auth/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { listAttractions, listTickets, listEmployees, listReservations } from '../api/endpoints';

export default function Dashboard() {
    const { user, token } = useAuth();
    const { data: attractions = [] } = useQuery({ queryKey:['attractions'], queryFn: listAttractions });
    const { data: tickets = [] } = useQuery({ queryKey:['tickets'], queryFn: () => listTickets(token!), enabled: !!token, });
    const { data: employees = [] } = useQuery({ queryKey:['employees'], queryFn: () => listEmployees(token!), enabled: !!token, });
    const { data: reservations = [] } = useQuery({ queryKey:['reservations'], queryFn: () => listReservations(token!), enabled: !!token, });

    return (
        <div>
            <h2>Tableau de bord</h2>
            <p>Bonjour, {user?.name}</p>
            <div className="card">
                <strong>Stats rapides</strong>
                <ul>
                    <li>Attractions: {attractions.length}</li>
                    <li>Tickets: {tickets.length}</li>
                    <li>Employees: {employees.length}</li>
                    <li>Reservations: {reservations.length}</li>
                </ul>
            </div>
        </div>
    );
};