import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobCardComponent } from './job-card.component';

describe('JobCardComponent', () => {
  let component: JobCardComponent;
  let fixture: ComponentFixture<JobCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(JobCardComponent);
    component = fixture.componentInstance;
    // mock job input
    component.job = {
      uuid: '1',
      title: 'Staff Software Engineer, EvilCorp',
      summary: 'EvilCorp is looking for the best of the best software engineers to ensure world dominance. Join our team to be part of it!'
    }
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render given title and summary in the job card', () => {
    const element = fixture.nativeElement;

    const title = element.querySelector('.title');
    const summary = element.querySelector('.summary');
    expect(title.textContent).toBe('Staff Software Engineer, EvilCorp');
    expect(summary.textContent).toBe('EvilCorp is looking for the best of the best software engineers to ensure world dominance. Join our team to be part of it!')
  })
});
