import { createBrowserRouter } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AttractionsList from './pages/attractions/AttractionsList';
import AttractionDetail from './pages/attractions/AttractionDetail';
import AttractionForm from './pages/attractions/AttractionForm';
import TicketsList from './pages/tickets/TicketsList';
import TicketDetail from './pages/tickets/TicketDetail';
import TicketForm from './pages/tickets/TicketForm';
import EmployeeList from './pages/employees/EmployeesList';
import EmployeeDetail from './pages/employees/EmployeeDetail';
import EmployeeForm from './pages/employees/EmployeeForm';
import ReservationsList from './pages/reservations/ReservationsList';
import ReservationDetail from './pages/reservations/ReservationDetail';
import ReservationForm from './pages/reservations/ReservationForm';
import ProtectedRoute from './auth/ProtectedRoute';

export const router = createBrowserRouter([
    {
        path: '/',
        element: <Layout />,
        children: [
            { index: true, element: <Home /> },
            { path: 'login', element: <Login /> },
            { path: 'register', element: <Register /> },

            {
                path: 'dashboard',
                element: (
                    <ProtectedRoute roles={['admin', 'employee', 'user']}>
                        <Dashboard />
                    </ProtectedRoute>
                )
            },

            // === ATTRACTIONS ===
            {
                path: 'attractions',
                children: [
                    { index: true, element: <AttractionsList /> },
                    { path: ':id', element: <AttractionDetail /> },
                    {
                        path: 'new',
                        element: (
                            <ProtectedRoute roles={['admin']}>
                                <AttractionForm />
                            </ProtectedRoute>
                        )
                    },
                    {
                        path: ':id/edit',
                        element: (
                            <ProtectedRoute roles={['admin']}>
                                <AttractionForm />
                            </ProtectedRoute>
                        )
                    },
                ],
            },

            // === TICKETS ===
            {
                path: 'tickets',
                children: [
                    { index: true, element: <ProtectedRoute><TicketsList /></ProtectedRoute> },
                    { path: ':id', element: <ProtectedRoute><TicketDetail /></ProtectedRoute> },
                    {
                        path: 'new',
                        element: (
                            <ProtectedRoute roles={['admin']}>
                                <TicketForm />
                            </ProtectedRoute>
                        )
                    },
                    {
                        path: ':id/edit',
                        element: (
                            <ProtectedRoute roles={['admin']}>
                                <TicketForm />
                            </ProtectedRoute>
                        )
                    },
                ]
            },

            // === EMPLOYEES ===
            {
                path: 'employees',
                children: [
                    { index: true, element: <ProtectedRoute roles={['admin']}><EmployeeList /></ProtectedRoute> },
                    { path: ':id', element: <ProtectedRoute roles={['admin']}><EmployeeDetail /></ProtectedRoute> },
                    { path: 'new', element: <ProtectedRoute roles={['admin']}><EmployeeForm /></ProtectedRoute> },
                    { path: ':id/edit', element: <ProtectedRoute roles={['admin']}><EmployeeForm /></ProtectedRoute> },
                ]
            },

            // === RESERVATIONS ===
            {
                path: 'reservations',
                children: [
                    { index: true, element: <ProtectedRoute><ReservationsList /></ProtectedRoute> },
                    { path: ':id', element: <ProtectedRoute><ReservationDetail /></ProtectedRoute> },
                    { path: 'new', element: <ProtectedRoute roles={['user']}><ReservationForm /></ProtectedRoute> },
                    { path: ':id/edit', element: <ProtectedRoute roles={['admin', 'user']}><ReservationForm /></ProtectedRoute> },
                ]
            },
        ]
    }
]);