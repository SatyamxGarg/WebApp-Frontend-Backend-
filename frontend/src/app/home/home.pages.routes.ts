import { Routes } from '@angular/router';

export const homeRoutes: Routes = [
    {
        path: 'extract',
        loadComponent: () => import('./pages/extract/extract.component').then(m => m.ExtractComponent),
    },
    { path: '', redirectTo: 'extract', pathMatch: 'full' },
];
