import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from "@angular/router/testing";

import { JobComponent } from './job.component';

describe('JobComponent', () => {
  let component: JobComponent;
  let fixture: ComponentFixture<JobComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, JobComponent],
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(JobComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create Job component', () => {
    expect(component).toBeTruthy();
  });
});
