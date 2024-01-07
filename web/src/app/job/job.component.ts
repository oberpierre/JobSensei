import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { of } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { NbCardModule } from '@nebular/theme';
import { Apollo, gql } from 'apollo-angular';
import { Job } from '../job';

export const GET_JOB = gql`
  query GetJob($uuid: String!) {
    job(uuid: $uuid) {
      title
    }
  }
`;

@Component({
  selector: 'app-job',
  standalone: true,
  imports: [NbCardModule, CommonModule],
  templateUrl: './job.component.html',
  styleUrl: './job.component.css'
})
export class JobComponent {
  job: Job | undefined;
  loading: boolean = true;
  error: any;

  constructor(private route: ActivatedRoute, private apollo: Apollo) {}

  ngOnInit() {
    this.route.paramMap.pipe(
      switchMap((params: ParamMap) => {
        const id = params.get('id');
        return of(id ? id : "");
      })
    ).subscribe((uuid) => {
      this.apollo
        .watchQuery<{job: Job}>({
          query: GET_JOB,
          variables: {
            uuid: uuid,
          }
        })
        .valueChanges.subscribe(({data, error, loading}) => {
          this.job = data?.job ?? undefined;
          this.loading = loading;
          this.error = error;
        });
    });
  }
}
