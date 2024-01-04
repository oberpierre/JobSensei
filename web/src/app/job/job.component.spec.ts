import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of } from 'rxjs';

import { JobComponent } from './job.component';

describe('JobComponent', () => {
  let component: JobComponent;
  let fixture: ComponentFixture<JobComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, JobComponent],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            paramMap: of(convertToParamMap({id: 'a0c1fe12-cec2-442a-9329-2cb47f761303'})),
          }
        }
      ]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(JobComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create Job component', () => {
    expect(component).toBeTruthy();
  });
  it('should display job id from url param', () => {
    expect(fixture.nativeElement.textContent).toBe('job works! id: a0c1fe12-cec2-442a-9329-2cb47f761303')
  })
});
