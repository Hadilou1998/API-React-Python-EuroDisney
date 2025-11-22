// ===== ROLES =====
export type Role = 'user' | 'employee' | 'admin';

// ===== USER =====
export interface User {
    id: number;
    name: string;
    email: string;
    role: Role;
}

export interface LoginPayload {
    email: string;
    password: string;
}

export interface RegisterPayload {
    name: string;
    email: string;
    password: string;
}

export interface LoginResponse {
    access_token: string;
    token_type: 'bearer';
    user: {
        id: number;
        name: string;
        email: string;
        role: Role;
    };
}

// ===== ATTRACTIONS =====
export type AttractionStatus = 'open' | 'closed' | 'maintenance';

export interface Attraction {
    id: number;
    name: string;
    description: string;
    capacity: number;
    status: AttractionStatus;
}

export interface CreateAttractionPayload {
    name: string;
    description: string;
    capacity: number;
    status: AttractionStatus;
}

export interface UpdateAttractionPayload {
    name?: string;
    description?: string;
    capacity?: number;
    status?: AttractionStatus;
}

// ===== TICKETS =====
export interface Ticket {
    id: number;
    user_id: number;
    attraction_id: number;
    date: string;
    qr_code: string;
    status?: string;
}

export interface CreateTicketPayload {
    user_id: number;
    attraction_id: number;
    date: string;
    qr_code: string;
}

export interface UpdateTicketPayload {
    user_id?: number;
    attraction_id?: number;
    date?: string;
    qr_code?: string;
}

// ===== RESERVATIONS =====
export interface Reservation {
    id: number;
    user_id: number;
    resource_type: string;
    date: string;
    nb_persons: number;
    status: 'pending' | 'confirmed' | 'cancelled';
}

export interface CreateReservationPayload {
    resource_type: string;
    date: string;
    nb_persons: number;
    status: 'pending' | 'confirmed' | 'cancelled';
}

export interface UpdateReservationPayload {
    resource_type?: string;
    date?: string;
    nb_persons?: number;
    status?: 'pending' | 'confirmed' | 'cancelled';
}

// ===== EMPLOYEES =====

export interface Employee {
    id: number;
    name: string;
    job: string;
    assignment: string | null;
}

export interface CreateEmployeePayload {
    name: string;
    job: string;
    assignment: string | null;
    password: string;
}

export interface UpdateEmployeePayload {
    name?: string;
    job?: string;
    assignment?: string | null;
}