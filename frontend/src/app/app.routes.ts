import { Routes } from '@angular/router';
// import { authGuard, nonAuthGuard } from './guards/auth.guard';
import { authRoutes } from './auth/auth-pages.routes';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'auth',
    pathMatch: 'full',
  },
  {
    path: 'auth',
    loadComponent: () => import('./auth/layout/layout.component').then(m => m.LayoutComponent),
    loadChildren: () => authRoutes,
    // canActivate: [nonAuthGuard],
  },
  {
    path: 'home',
    loadChildren: () => import('./home/home.pages.routes').then(m => m.homeRoutes),
  },
];
