import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getAttraction } from '../../api/endpoints';

export default function AttractionDetail() {
    const { id } = useParams();
    const number = Number(id);
    const { data, isLoading, error } = useQuery({ queryKey: ['attraction', number], queryFn: () => getAttraction(number), enabled: !!number });
    if (!number) return <p>Invalid</p>
    if (isLoading) return <p>Loading...</p>
    if (error) return <p>Error</p>

    return (
        <div className="card">
            <h2>{data?.name}</h2>
            <p>{data?.description}</p>
            <p>Capacity: {data?.capacity}</p>
            <p>Status: {data?.status}</p>
        </div>
    )
};