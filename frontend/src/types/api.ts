export type Role = 'user' | 'employee' | 'admin'

export interface User { id: number; name: string; email: string; role: Role }

export interface LoginPayload { email: string; password: string }
export interface RegisterPayload { name: string; email: string; password: string }
export interface LoginResponse { access_token: string; token_type: 'bearer'; user: User }

export type AttractionStatus = 'open' | 'closed' | 'maintenance'
export interface Attraction { id: number; name: string; description: string; capacity: number; status: AttractionStatus; }
export interface CreateAttractionPayload extends Omit<Attraction, 'id'> { id: number; name: string; description: string; capacity: number; status: AttractionStatus; }
export interface UpdateAttractionPayload extends Partial<CreateAttractionPayload> { id: number; name: string; description: string; capacity: number; status: AttractionStatus; }

export interface Ticket { id: number; user_id: number; attraction_id: number; date: string; qr_code: string; status?: string; }
export interface Reservation { id: number; user_id: number; resource_type: string; date: string; nb_persons: number; status: 'pending' | 'confirmed' | 'cancelled' }
export interface Employee { id: number; name: string; job: string; assignment: string; }
export interface CreateEmployeePayload extends Omit<Employee, 'id'> { id: number; name: string; job: string; assignment: string; }
export interface UpdateEmployeePayload extends Partial<CreateEmployeePayload> { id: number; name: string; job: string; assignment: string; }