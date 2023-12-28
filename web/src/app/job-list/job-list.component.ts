import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NbCardModule, NbListModule } from '@nebular/theme';
import { JobCardComponent } from '../job-card/job-card.component';
import { Job } from '../job';
import { JobsService } from '../jobs.service';

@Component({
  selector: 'app-job-list',
  standalone: true,
  imports: [
    CommonModule,
    NbCardModule,
    NbListModule,
    JobCardComponent,
  ],
  templateUrl: './job-list.component.html',
  styleUrl: './job-list.component.css'
})
export class JobListComponent {
  jobs: Job[] = [];

  constructor(private jobsService: JobsService) {}

  ngOnInit(): void {
    this.initJobs();
  }

  initJobs(): void {
    this.jobsService.getJobs().subscribe((jobs) => this.jobs = jobs); 
  }
}
