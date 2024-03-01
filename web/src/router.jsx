import { createBrowserRouter } from 'react-router-dom';
import NotMatch from 'component/common/route/not_match';
import PrivateRoute from 'component/common/route/private_route.jsx';
import BlankLayout from 'component/common/layout/blank';
import MainLayout from 'component/common/layout/main';

import App from 'src/app';

const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        children: [
            {
                path: 'login',
                element: <BlankLayout />,
                children: [
                    {
                        path: '',
                        lazy: async () => ({
                            Component: (await import('component/auth/basic_auth/login'))
                                .default
                        })
                    }
                ]
            },
            {
                path: '',
                element: <MainLayout />,
                children: [
                    {
                        path: '',
                        element: <PrivateRoute />,
                        children: [
                            {
                                path: '',
                                lazy: async () => ({
                                    Component: (
                                        await import('component/account/profile')
                                    ).default
                                })
                            },
                            {
                                path: 'account/user',
                                lazy: async () => ({
                                    Component: (await import('component/account/user'))
                                        .default
                                })
                            },
                            {
                                path: 'account/role',
                                lazy: async () => ({
                                    Component: (await import('component/account/role'))
                                        .default
                                })
                            },
                            {
                                path: 'config/variable',
                                lazy: async () => ({
                                    Component: (
                                        await import('component/config/variable')
                                    ).default
                                })
                            }
                        ]
                    }
                ]
            },
            {
                path: '*',
                element: <NotMatch />
            }
        ]
    }
]);
export default router;
