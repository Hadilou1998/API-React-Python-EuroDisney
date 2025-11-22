import api from './axios';
import type {
    LoginPayload,
    LoginResponse,
    RegisterPayload,
    Attraction,
    Ticket,
    CreateTicketPayload,
    UpdateTicketPayload,
    Employee,
    Reservation,
    CreateReservationPayload,
    UpdateReservationPayload,
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

// === Helper for add token ===
const authHeader = (token?: string) => ({
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
});

// === Users ===
export const getUserTickets = (userId: number, token: string) =>
    api.get<Ticket[]>(`/users/${userId}/tickets`, { headers: authHeader(token), withCredentials: true }).then(r => r.data);

// === Attraction ===
export const listAttractions = () => api.get<Attraction[]>('/attractions/', { withCredentials: true }).then(r => r.data);
export const getAttraction = (id: number) => api.get<Attraction>(`/attractions/${id}`, { withCredentials: true }).then(r => r.data);
export const createAttraction = (p: CreateAttractionPayload, token: string) => api.post('/attractions/new', p, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const updateAttraction = (id: number, p: UpdateAttractionPayload, token: string) => api.put(`/attractions/${id}`, p, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const deleteAttraction = (id: number, token: string) => api.delete(`/attractions/${id}`, { headers: authHeader(token), withCredentials: true }).then(r => r.data);

// === Tickets ===
export const listTickets = (token: string) => api.get<Ticket[]>('/tickets/', { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const getTicket = (id: number, token: string) => api.get<Ticket>(`/tickets/${id}`, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const createTicket = (p: CreateTicketPayload, token: string) => api.post('/tickets/new', p, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const updateTicket = (id: number, p: UpdateTicketPayload, token: string) => api.put(`/tickets/${id}`, p, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const deleteTicket = (id: number, token: string) => api.delete(`/tickets/${id}`, { headers: authHeader(token), withCredentials: true }).then(r => r.data);

// === Employees ===
export const listEmployees = (token: string) => api.get<Employee[]>('/employees/', { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const getEmployee = (id: number, token: string) => api.get<Employee>(`/employees/${id}`, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const createEmployee = (p: CreateEmployeePayload, token: string) => api.post('/employees/new', p, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const updateEmployee = (id: number, p: UpdateEmployeePayload, token: string) => api.put(`/employees/${id}`, p, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const deleteEmployee = (id: number, token: string) => api.delete(`/employees/${id}`, { headers: authHeader(token), withCredentials: true }).then(r => r.data);

// === Reservations ===
export const listReservations = (token: string) => api.get<Reservation[]>('/reservations/', { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const getReservation = (id: number, token: string) => api.get<Reservation>(`/reservations/${id}`, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const createReservation = (p: CreateReservationPayload, token: string) => api.post('/reservations/new', p, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const updateReservation = (id: number, p: UpdateReservationPayload, token: string) => api.put(`/reservations/${id}`, p, { headers: authHeader(token), withCredentials: true }).then(r => r.data);
export const deleteReservation = (id: number, token: string) => api.delete(`/reservations/${id}`, { headers: authHeader(token), withCredentials: true }).then(r => r.data);