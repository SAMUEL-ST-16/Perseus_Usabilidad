import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./components/home/home').then((m) => m.HomeComponent),
  },
  {
    path: 'iso25010',
    loadComponent: () =>
      import('./components/iso25010/iso25010').then((m) => m.ISO25010Component),
  },
  {
    path: '**',
    redirectTo: '',
  },
];
