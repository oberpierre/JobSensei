import { Routes } from '@angular/router';
import { JobListComponent } from './job-list/job-list.component';

export const routes: Routes = [
    {path: 'jobs', component: JobListComponent},
    {path: '', redirectTo: '/jobs', pathMatch: 'full'},
];