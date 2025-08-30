import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createEmployee, listEmployees, updateEmployee } from '../../api/endpoints';

export default function EmployeeForm() {
    const { id } = useParams();
    const editing = Boolean(id);
    const nav = useNavigate();
    const [name, setName] = useState('');
    const [job, setJob] = useState('');
    const [assignment, setAssignment] = useState('');

    useEffect(() => {
        if (editing) {
            listEmployees().then(list => {
                const emp = list.find(x => x.id === Number(id));
                if (emp) {
                    setName(emp.name);
                    setJob(emp.job);
                    setAssignment(emp.assignment);
                }
            });
        }
    }, [editing, id]);

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (editing) {
            updateEmployee(Number(id), { id: Number(id), name, job, assignment }).then(() => {
                nav('/employees');
            });
        } else {
            createEmployee({ id: Number(id), name, job, assignment }).then(() => {
                nav('/employees');
            });
        }
    };

    return (
        <form className="card" onSubmit={onSubmit} style={{ maxWidth: 640 }}>
            <h2>{editing ? 'Update' : 'Create'} an Employee</h2>
            <label>Name</label>
            <input className="input" value={name} onChange={e => setName(e.target.value)} placeholder="Name" title="Name" />
            <label style={{ marginTop: 8 }}>Job</label>
            <input className="input" value={job} onChange={e => setJob(e.target.value)} placeholder="Job" title="Job" />
            <label style={{ marginTop: 8 }}>Assignment</label>
            <input className="input" value={assignment} onChange={e => setAssignment(e.target.value)} placeholder="Assignment" title="Assignment" />
            <div style={{ marginTop: 12 }}>
                <button className="btn primary">{editing ? 'Update' : 'Create'}</button>
            </div>
        </form>
    );
};