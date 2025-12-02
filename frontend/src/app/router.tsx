import { createBrowserRouter, Navigate } from 'react-router-dom'
import { AppLayout } from '@/components/layouts/AppLayout'
import Dashboard from '@/pages/Dashboard'
import Tickets from '@/pages/Tickets'
import TicketDetail from '@/pages/TicketDetail'
import Workflows from '@/pages/Workflows'
import Policies from '@/pages/Policies'
import Insights from '@/pages/Insights'
import Strategy from '@/pages/Strategy'
import Financial from '@/pages/Financial'
import Settings from '@/pages/Settings'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: 'dashboard',
        element: <Dashboard />,
      },
      {
        path: 'tickets',
        element: <Tickets />,
      },
      {
        path: 'tickets/:id',
        element: <TicketDetail />,
      },
      {
        path: 'workflows',
        element: <Workflows />,
      },
      {
        path: 'policies',
        element: <Policies />,
      },
      {
        path: 'insights',
        element: <Insights />,
      },
      {
        path: 'financial',
        element: <Financial />,
      },
      {
        path: 'strategy',
        element: <Strategy />,
      },
      {
        path: 'settings',
        element: <Settings />,
      },
    ],
  },
])
