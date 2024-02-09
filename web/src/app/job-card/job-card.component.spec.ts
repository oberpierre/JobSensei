import { By } from '@angular/platform-browser';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NbBadgeComponent, NbStatusService } from '@nebular/theme';

import { JobCardComponent } from './job-card.component';

class MockNbStatusService {
  isCustomStatus = () => false;
}

describe('JobCardComponent', () => {
  let component: JobCardComponent;
  let fixture: ComponentFixture<JobCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobCardComponent],
      providers: [
        {provide: NbStatusService, useClass: MockNbStatusService},
      ],
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(JobCardComponent);
    component = fixture.componentInstance;
  });

  it('should create job card component', () => {
    expect(component).toBeTruthy();
  });

  it('should render given title and summary in the job card', () => {
    component.job = {
      uuid: '1',
      title: 'Staff Software Engineer, EvilCorp',
      summary: 'EvilCorp is looking for the best of the best software engineers to ensure world dominance. Join our team to be part of it!'
    }

    fixture.detectChanges();
    const element = fixture.nativeElement;

    const title = element.querySelector('.title');
    const summary = element.querySelector('.summary');
    expect(title.textContent).toBe('Staff Software Engineer, EvilCorp');
    expect(summary.textContent).toBe('EvilCorp is looking for the best of the best software engineers to ensure world dominance. Join our team to be part of it!')
    const badge = fixture.debugElement.query(By.directive(NbBadgeComponent));
    expect(badge).toBeNull();
  });

  it('should display delisted badge if deletedOn is truthy', () => {
    component.job = {
      uuid: '1',
      title: 'Foobar',
      isDeleted: true,
    }

    fixture.detectChanges();
    const badge = fixture.debugElement.query(By.directive(NbBadgeComponent));
    expect(badge?.nativeElement?.textContent).toBe('Delisted');
  });

  it('should display recent badge if isRecent is true', () => {
    component.job = {
      uuid: '1',
      title: 'Foobar',
      isRecent: true,
    }

    fixture.detectChanges();
    const badge = fixture.debugElement.query(By.directive(NbBadgeComponent));
    expect(badge?.nativeElement?.textContent).toBe('Recent');
  });

  it('should display delisted badge on if deletedOn and isRecent are both truthy', () => {
    component.job = {
      uuid: '1',
      title: 'Foobar',
      isDeleted: true,
      isRecent: true,
    }

    fixture.detectChanges();
    const badge = fixture.debugElement.queryAll(By.directive(NbBadgeComponent));
    expect(badge.length).toBe(1);
    expect(badge?.[0]?.nativeElement?.textContent).toBe('Delisted');
  });
});
