import { Routes } from '@angular/router';
import { JobListComponent } from './job-list/job-list.component';
import { NotFoundComponent } from './not-found/not-found.component';

export const routes: Routes = [
    {path: 'jobs', component: JobListComponent},
    {path: '', redirectTo: '/jobs', pathMatch: 'full'},
    {path: '**', component: NotFoundComponent}
];