import { Routes } from '@angular/router';

export const routes: Routes = [
    {path: 'jobs', loadComponent: () => import('./job-list/job-list.component').then(mod => mod.JobListComponent)},
    {path: 'job/:id', loadComponent: () => import('./job/job.component').then(mod => mod.JobComponent)},
    {path: '', redirectTo: '/jobs', pathMatch: 'full'},
    {path: '**', loadComponent: () => import('./not-found/not-found.component').then(mod => mod.NotFoundComponent)}
];