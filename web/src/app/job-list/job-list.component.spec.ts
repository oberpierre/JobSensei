import { By } from '@angular/platform-browser';
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { JobListComponent } from './job-list.component';
import { NbStatusService } from '@nebular/theme';
import { JobCardComponent } from '../job-card/job-card.component';

class MockNbStatusService {
  isCustomStatus = () => false;
}

describe('JobListComponent', () => {
  let component: JobListComponent;
  let fixture: ComponentFixture<JobListComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [JobListComponent],
      providers: [{provide: NbStatusService, useClass: MockNbStatusService}]
    })
    .compileComponents()
    .then(() => {
      fixture = TestBed.createComponent(JobListComponent);
      component = fixture.componentInstance;
      component.jobs = [
        {uuid: '1', title: 'foo', summary: 'bar'},
        {uuid: '2', title: 'fizzbuzz'}
      ];
      fixture.detectChanges();
    });
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should', () => {
    const cards = fixture.debugElement.queryAll(By.directive(JobCardComponent));
    const jobs = cards.map((card) => card.componentInstance.job);
    expect(jobs.length).toBe(2);
    expect(jobs[0]).toEqual({uuid: '1', title: 'foo', summary: 'bar'});
    expect(jobs[1]).toEqual({uuid: '2', title: 'fizzbuzz'});
  })
});
