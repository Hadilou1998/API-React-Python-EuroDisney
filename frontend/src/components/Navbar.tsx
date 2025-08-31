import { Link } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';

export default function Navbar() {
    const { user, logout } = useAuth();

    return (
        <nav className="nav">
            <Link to="/">EuroDisney</Link>
            <Link to="/dashboard">Home</Link>
            <Link to="/attractions">Attractions</Link>
            <Link to="/tickets">Tickets</Link>
            <Link to="/reservations">Reservations</Link>
            <Link to="/employees">Employees</Link>
            <div className="spacer" />
            {!user && <Link to="/login">Se connecter</Link>}
            {!user && <Link to="/register">S'inscrire</Link>}
            {user && <span>Welcome, {user.name} ({user.role})!</span>}
            {user && <button className='btn' onClick={logout}>Se déconnecter</button>}
        </nav>
    );
};