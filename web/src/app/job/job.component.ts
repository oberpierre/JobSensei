import { Component } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { of } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { NbButtonModule, NbCardModule, NbIconModule, NbSpinnerModule, NbTagModule } from '@nebular/theme';
import { Apollo, gql } from 'apollo-angular';
import { Job } from '../job';

export const GET_JOB = gql`
  query GetJob($uuid: String!) {
    job(uuid: $uuid) {
      title
      summary
      url
      locations {
        city
        country
      }
      skills
      responsibilities
      qualifications {
        required
        preferred
      }
    }
  }
`;

@Component({
  selector: 'app-job',
  standalone: true,
  imports: [
    CommonModule,
    NbButtonModule,
    NbCardModule,
    NbIconModule,
    NbSpinnerModule,
    NbTagModule,
  ],
  templateUrl: './job.component.html',
  styleUrl: './job.component.css'
})
export class JobComponent {
  job: Job | undefined;
  loading: boolean = true;
  error: any;

  constructor(private route: ActivatedRoute, private apollo: Apollo, private location: Location) {}

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

  goBack() {
    this.location.back();
  }
}
