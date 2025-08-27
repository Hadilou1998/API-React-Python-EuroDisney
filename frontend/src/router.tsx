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
import EmployeeList from './pages/employees/EmployeeList';
import EmployeeForm from './pages/employees/EmployeeForm';
import ReservationsList from './pages/reservations/ReservationsList';
import ProtectedRoute from './auth/ProtectedRoute';

export const router = createBrowserRouter([
    {
        path: '/',
        element: <Layout />,
        children: [
            { index: true, element: <Home /> },
            { path: 'login', element: <Login /> },
            { path:'register', element: <Register /> },

            {
                path: 'dashboard',
                element: (
                    <ProtectedRoute roles={['admin', 'employee', 'user']}>
                        <Dashboard />
                    </ProtectedRoute>
                )
            },

            // Attractions (admin)
            {
                path: 'attractions',
                children: [
                    { index: true, element: <AttractionsList /> },
                    {
                        path: 'id',
                        element: <AttractionDetail />
                    },
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

            // Tickets
            { path: 'tickets', element: <ProtectedRoute><TicketsList /></ProtectedRoute> },
            { path: 'tickets/:id', element: <ProtectedRoute><TicketDetail /></ProtectedRoute> },

            // Employees (admin)
            {
                path: 'employees',
                children: [
                    { index: true, element: <ProtectedRoute roles={['admin']}><EmployeeList /></ProtectedRoute> },
                    { path: 'new', element: <ProtectedRoute roles={['admin']}><EmployeeForm /></ProtectedRoute> },
                    { path: ':id/edit', element: <ProtectedRoute roles={['admin']}><EmployeeForm /></ProtectedRoute> },
                ]
            },

            // Reservations
            { path: 'reservations', element: <ProtectedRoute><ReservationsList /></ProtectedRoute> },
        ]
    }
]);