import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NbCardModule, NbListModule } from '@nebular/theme';
import { JobCardComponent } from '../job-card/job-card.component';
import { Job } from '../job';
import { Apollo, gql } from 'apollo-angular';

export const GET_JOBS = gql`
  query GetJobs {
    jobs {
      uuid
      title
      summary
      deletedOn
    }
  }
`;

@Component({
  selector: 'app-job-list',
  standalone: true,
  imports: [
    RouterModule,
    CommonModule,
    NbCardModule,
    NbListModule,
    JobCardComponent,
  ],
  templateUrl: './job-list.component.html',
  styleUrl: './job-list.component.css'
})
export class JobListComponent {
  jobs: Job[] | null = null;
  loading: boolean = true;
  error: any;

  constructor(private apollo: Apollo) {}

  ngOnInit(): void {
    this.initJobs();
  }

  initJobs(): void {
    this.apollo
      .watchQuery<{jobs: Job[]}>({
        query: GET_JOBS,
      })
      .valueChanges.subscribe(({data, error, loading}) => {
        this.jobs = data?.jobs ?? null;
        this.loading = loading;
        this.error = error;
      }); 
  }
}
