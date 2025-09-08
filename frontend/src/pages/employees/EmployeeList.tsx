import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { deleteEmployee, listEmployees } from '../../api/endpoints';
import { useAuth } from '../../auth/AuthContext';

export default function EmployeeList() {
    const nav = useNavigate();
    const queryClient = useQueryClient();
    const { token } = useAuth(); 
    
    const { data, isLoading } = useQuery({ 
        queryKey: ['employees'], 
        queryFn: () => listEmployees(token!), 
        enabled: !!token,
    });
    
    const del = useMutation({
        mutationFn: (id: number) => deleteEmployee(id, token!),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['employees'] }),
    });

    if (isLoading) return <p>Loading...</p>;

    // Protection if data is not a array
    const employees = Array.isArray(data) ? data : [];
    
    return (
        <>
            <h2>Employees</h2>
            <button className="btn primary" onClick={() => nav('/new')}>Add</button>
            <table className="table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Job</th>
                        <th>Assignment</th>
                    </tr>
                </thead>
                <tbody>
                    {employees.length > 0 ? (
                        employees.map(emp => (
                            <tr key={emp.id}>
                                <td>{emp.name}</td>
                                <td>{emp.job}</td>
                                <td>{emp.assignment}</td>
                                <td style={{ display: 'flex', gap:8 }}>
                                    <button className='btn' onClick={() => nav(`/${emp.id}/edit`)}>Edit</button>
                                    <button className="btn" onClick={() => del.mutate(emp.id)}>Delete</button>
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan={4}>No employees available</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </>
    );
};