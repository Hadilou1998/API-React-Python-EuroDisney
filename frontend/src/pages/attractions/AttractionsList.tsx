import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link, useNavigate } from 'react-router-dom';
import { deleteAttraction, listAttractions } from '../../api/endpoints';
import { useAuth } from '../../auth/AuthContext';

export default function AttractionsList() {
    const queryClient = useQueryClient();
    const nav = useNavigate();
    const { user } = useAuth();
    const { data, isLoading, error } = useQuery({ queryKey:['attractions'], queryFn: listAttractions });
    const del = useMutation({
        mutationFn: (id: number) => deleteAttraction(id),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['attractions'] })
    });

    if (isLoading) return <p>Loading...</p>;
    if (error) return <p>Error</p>;

    return (
        <div>
            <h2>Attractions</h2>
            {user?.role === 'admin' && <button className="btn primary" onClick={() => nav('/attractions/new')}>Add</button>}
            <div className="card">
                {data?.map(a => (
                    <div key={a.id} className="card">
                        <h3><Link to={`/attractions/${a.id}`}>{a.name}</Link></h3>
                        <p>{a.description}</p>
                        <p>Capacity: {a.capacity} - Status: {a.status}</p>
                        {user?.role === 'admin' && (
                            <div className="actions">
                                <button className="btn" onClick={() => nav(`/attractions/${a.id}/edit`)}>Update</button>
                                <button className="btn" onClick={() => del.mutate(a.id)}>Delete</button>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};