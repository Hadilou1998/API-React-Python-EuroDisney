import api from './axios';
import type {
    LoginPayload,
    LoginResponse,
    RegisterPayload,
    Attraction,
    Ticket,
    Employee,
    Reservation,
    CreateAttractionPayload,
    UpdateAttractionPayload,
    CreateEmployeePayload,
    UpdateEmployeePayload
} from '../types/api';

// === Auth ===
// FastAPI OAuth2PasswordRequestForm attend username et password en x-www-form-urlencoded
export const login = (p: LoginPayload) => {
    const formData = new URLSearchParams();
    formData.append("username", p.email);  // FastAPI s'attend à "username"
    formData.append("password", p.password);

    return api.post<LoginResponse>("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        withCredentials: true, // si on gère les cookies
    }).then(r => r.data);
};

export const register = (p: RegisterPayload) =>
    api.post('/auth/register', p, { withCredentials: true }).then(r => r.data);

// === Users ===
export const getUserTickets = (userId: number) =>
    api.get<Ticket[]>(`/users/${userId}/tickets`, { withCredentials: true }).then(r => r.data);

// === Attraction ===
export const listAttractions = () => api.get<Attraction[]>('/attractions', { withCredentials: true }).then(r => r.data);
export const getAttraction = (id: number) => api.get<Attraction>(`/attractions/${id}`, { withCredentials: true }).then(r => r.data);
export const createAttraction = (p: CreateAttractionPayload) => api.post('/attractions', p, { withCredentials: true }).then(r => r.data);
export const updateAttraction = (id: number, p: UpdateAttractionPayload) => api.put(`/attractions/${id}`, p, { withCredentials: true }).then(r => r.data);
export const deleteAttraction = (id: number) => api.delete(`/attractions/${id}`, { withCredentials: true }).then(r => r.data);

// === Tickets ===
export const listTickets = () => api.get<Ticket[]>('/tickets', { withCredentials: true }).then(r => r.data);
export const getTicket = (id: number) => api.get<Ticket>(`/tickets/${id}`, { withCredentials: true }).then(r => r.data);

// === Employees ===
export const listEmployees = () => api.get<Employee[]>('/employees', { withCredentials: true }).then(r => r.data);
export const getEmployee = (id: number) => api.get<Employee>(`/employees/${id}`, { withCredentials: true }).then(r => r.data);
export const createEmployee = (p: CreateEmployeePayload) => api.post('/employees', p, { withCredentials: true }).then(r => r.data);
export const updateEmployee = (id: number, p: UpdateEmployeePayload) => api.put(`/employees/${id}`, p, { withCredentials: true }).then(r => r.data);
export const deleteEmployee = (id: number) => api.delete(`/employees/${id}`, { withCredentials: true }).then(r => r.data);

// === Reservations ===
export const listReservations = () => api.get<Reservation[]>('/reservations', { withCredentials: true }).then(r => r.data);