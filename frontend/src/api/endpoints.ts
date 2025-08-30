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

// Auth
export const login = (p: LoginPayload) => api.post<LoginResponse>('/auth/login', p).then(r => r.data);
export const register = (p: RegisterPayload) => api.post('/auth/register', p).then(r => r.data);

// Users
export const getUserTickets = (userId: number) => api.get<Ticket[]>(`/users/${userId}/tickets`).then(r => r.data);

// Attraction
export const listAttractions = () => api.get<Attraction[]>('/attractions').then(r => r.data);
export const getAttraction = (id: number) => api.get<Attraction>(`/attractions/${id}`).then(r => r.data);
export const createAttraction = (p: CreateAttractionPayload) => api.post('/attractions', p).then(r => r.data);
export const updateAttraction = (id: number, p: UpdateAttractionPayload) => api.put(`/attractions/${id}`, p).then(r => r.data);
export const deleteAttraction = (id: number) => api.delete(`/attractions/${id}`).then(r => r.data);

// Tickets
export const listTickets = () => api.get<Ticket[]>('/tickets').then(r => r.data);
export const getTicket = (id: number) => api.get<Ticket>(`/tickets/${id}`).then(r => r.data);

// Employees
export const listEmployees = () => api.get<Employee[]>('/employees').then(r => r.data);
export const getEmployee = (id: number) => api.get<Employee>(`/employees/${id}`).then(r => r.data);
export const createEmployee = (p: CreateEmployeePayload) => api.post('/employees', p).then(r => r.data);
export const updateEmployee = (id: number, p: UpdateEmployeePayload) => api.put(`/employees/${id}`, p).then(r => r.data);
export const deleteEmployee = (id: number) => api.delete(`/employees/${id}`).then(r => r.data);

// Reservations
export const listReservations = () => api.get<Reservation[]>('/reservations').then(r => r.data);