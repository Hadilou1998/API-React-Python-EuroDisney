import { useAuth } from '../auth/AuthContext';

export default function Home() {
    const { user } = useAuth();
    
    return (
        <div className="card">
            <h1>Bienvenue à EuroDisney {user?.role}</h1>
            <p>Gérez attractions, billets, réservations et autres aspects de votre parc d'attractions EuroDisney</p>
        </div>
    );
};