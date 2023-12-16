import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobListComponent } from './job-list.component';
import { NbStatusService } from '@nebular/theme';

class MockNbStatusService {
  isCustomStatus = () => false;
}

describe('JobListComponent', () => {
  let component: JobListComponent;
  let fixture: ComponentFixture<JobListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      providers: [JobListComponent, {provide: NbStatusService, useClass: MockNbStatusService}]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(JobListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
