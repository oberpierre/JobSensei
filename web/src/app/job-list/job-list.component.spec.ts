import { By } from '@angular/platform-browser';
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { RouterTestingModule } from "@angular/router/testing";
import { ApolloTestingController, ApolloTestingModule } from 'apollo-angular/testing';
import { NbStatusService } from '@nebular/theme';

import { GET_JOBS, JobListComponent } from './job-list.component';
import { JobCardComponent } from '../job-card/job-card.component';

class MockNbStatusService {
  isCustomStatus = () => false;
}

describe('JobListComponent', () => {
  let component: JobListComponent;
  let fixture: ComponentFixture<JobListComponent>;
  let controller: ApolloTestingController;

  beforeEach(waitForAsync(() =>
    TestBed.configureTestingModule({
      imports: [RouterTestingModule, ApolloTestingModule, JobListComponent],
      providers: [
        {provide: NbStatusService, useClass: MockNbStatusService},
      ]
    })
    .compileComponents()
    .then(() => {
      fixture = TestBed.createComponent(JobListComponent);
      component = fixture.componentInstance;
      fixture.detectChanges();

      controller = TestBed.inject(ApolloTestingController);
    })
  ));

  afterEach(() => {
    controller.verify();
  });

  it('should create JobList component', async () => {
    const op = controller.expectOne(GET_JOBS);
    op.flush({
      data: {
        jobs: []
      },
    });

    await fixture.whenStable();

    expect(component).toBeTruthy();
  });

  it('should show loading and create cards for fetched jobs', async () => {
    const op = controller.expectOne(GET_JOBS);
    op.flush({
      data: {
        jobs: [
          {uuid: '1', title: 'foo', summary: 'foobar', isRecent: false, isDeleted: true},
          {uuid: '2', title: 'fizzbuzz', summary: null, isRecent: true, isDeleted: false}
        ]
      },
    });

    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).toBe("Loading...");
    
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).not.toBe("Loading...");

    const cards = fixture.debugElement.queryAll(By.directive(JobCardComponent));
    const jobs = cards.map((card) => card.componentInstance.job);
    expect(jobs.length).toBe(2);
    expect(jobs[0]).toEqual({uuid: '1', title: 'foo', summary: 'foobar', isRecent: false, isDeleted: true});
    expect(jobs[1]).toEqual({uuid: '2', title: 'fizzbuzz', summary: null, isRecent: true, isDeleted: false});
  });
});
