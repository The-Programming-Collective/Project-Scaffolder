import { Routes } from '@angular/router';

export const appRoutes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'counter-feature',
    loadChildren: () =>
      import('./features/counter/counter.module').then((m) => m.CounterModule),
  },
];
