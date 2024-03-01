import * as React from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { RecoilRoot } from 'recoil';
import 'service/styles/main.css';
import router from './router';

createRoot(document.getElementById('root')).render(
    <RecoilRoot>
        <RouterProvider router={router} />
    </RecoilRoot>
);
