import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { Observable, of } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-job',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './job.component.html',
  styleUrl: './job.component.css'
})
export class JobComponent {
  jobId$: Observable<string> | undefined;

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.jobId$ = this.route.paramMap.pipe(
      switchMap((params: ParamMap) => {
        const id = params.get('id');
        return of(id ? id : "");
      })
    );
  }
}
