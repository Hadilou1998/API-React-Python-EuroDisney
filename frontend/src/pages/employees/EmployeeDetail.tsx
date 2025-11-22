import { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { deleteEmployee, getEmployee } from '../../api/endpoints';
import { useAuth } from '../../auth/AuthContext';
import type { Employee } from '../../types/api';

export default function EmployeeDetail() {
    const { id } = useParams();
    const { token, user } = useAuth();
    const nav = useNavigate();

    const [emp, setEmp] = useState<Employee | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!token) return;
        getEmployee(Number(id), token)
            .then(setEmp)
            .finally(() => setLoading(false));
    }, [id, token]);

    if (loading) return <p>Loading...</p>;
    if (!emp) return <p>Employee not found</p>;

    const isAdmin = user?.role === "admin";

    const handleDelete = async () => {
        if (!window.confirm("Are you sure?")) return;
        await deleteEmployee(emp.id, token || "");
        nav('/employees');
    };

    return (
        <div className="card" style={{ maxWidth: 600 }}>
            <h2>Employee #{emp.id}</h2>

            <p><b>Name:</b> {emp.name}</p>
            <p><b>Job:</b> {emp.job}</p>
            <p><b>Assignment:</b> {emp.assignment}</p>

            <div style={{ marginTop: 16 }}>
                <Link to="/employees" className="btn">Back</Link>

                {isAdmin && (
                    <>
                        <Link to={`/employees/${emp.id}/edit`} className="btn primary" style={{ marginLeft: 8 }}>
                            Edit
                        </Link>

                        <button className="btn danger" style={{ marginLeft: 8 }} onClick={handleDelete}>
                            Delete
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}