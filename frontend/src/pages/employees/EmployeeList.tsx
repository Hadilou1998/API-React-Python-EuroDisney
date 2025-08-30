import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { deleteEmployee, listEmployees } from '../../api/endpoints';

export default function EmployeeList() {
    const nav = useNavigate();
    const queryClient = useQueryClient();
    const { data, isLoading } = useQuery({ queryKey: ['employees'], queryFn: listEmployees });
    const del = useMutation({
        mutationFn: (id: number) => deleteEmployee(id),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['employees'] })
    });
    if (isLoading) return <p>Loading...</p>;
    
    return (
        <>
            <h2>Employees</h2>
            <button className="btn primary" onClick={() => nav('/employees/new')}>Add</button>
            <table className="table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Job</th>
                        <th>Assignment</th>
                    </tr>
                </thead>
                <tbody>
                    {data?.map((emp) => (
                        <tr key={emp.id}>
                            <td>{emp.name}</td>
                            <td>{emp.job}</td>
                            <td>{emp.assignment}</td>
                            <td style={{ display: 'flex', gap:8 }}>
                                <button className='btn' onClick={() => nav(`/employees/${emp.id}/edit`)}>Edit</button>
                                <button className="btn" onClick={() => del.mutate(emp.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    );
};