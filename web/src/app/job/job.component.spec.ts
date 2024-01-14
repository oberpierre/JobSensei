import { By } from '@angular/platform-browser';
import { Component } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of } from 'rxjs';
import { ApolloTestingController, ApolloTestingModule } from 'apollo-angular/testing';
import { NbFocusMonitor, NbStatusService, NbSpinnerComponent, NbTagListComponent } from '@nebular/theme';

import { JobComponent, GET_JOB } from './job.component';

class MockNbStatusService {
  isCustomStatus = () => false;
}
class MockNbFocusMonitor {}
@Component({standalone: true, selector: 'nb-tag-list', template: ''})
class MockNbTagListComponent {}
describe('JobComponent', () => {
  let component: JobComponent;
  let fixture: ComponentFixture<JobComponent>;
  let controller: ApolloTestingController;

  beforeEach(async () => {
    const nbActiveDescendantKeyManagerFactoryService = jasmine.createSpyObj('NbActiveDescendantKeyManagerFactoryService', ['']);

    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, ApolloTestingModule, MockNbTagListComponent, JobComponent],
      providers: [
        {provide: NbStatusService, useClass: MockNbStatusService},
        {provide: NbFocusMonitor, useClass: MockNbFocusMonitor},
        {provide: 'NbActiveDescendantKeyManagerFactoryService', useValue: nbActiveDescendantKeyManagerFactoryService},
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

    controller = TestBed.inject(ApolloTestingController);
  });

  it('should create Job component', () => {
    const op = controller.expectOne(GET_JOB);
    op.flush({
      data: {
        job: null
      },
    });

    expect(component).toBeTruthy();
  });
  it('should fetch job and display details', async () => {
    const op = controller.expectOne(GET_JOB);
    op.flush({
      data: {
        job: {
          title: 'foobar',
          summary: null,
          url: null,
          locations: null,
          skills: null,
          responsibilities: null,
          qualifications: null,
        },
      },
    });

    await fixture.whenStable();

    expect(op.operation.variables['uuid']).toBe('a0c1fe12-cec2-442a-9329-2cb47f761303');
    expect(fixture.debugElement.query(By.directive(NbSpinnerComponent))).toBeTruthy();

    fixture.detectChanges();

    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('h2')?.textContent).toBe('foobar')
    expect(fixture.debugElement.query(By.directive(NbSpinnerComponent))).toBeFalsy();
    const sectionHeaders = element.querySelectorAll('h3');
    expect(sectionHeaders.length).toBe(0);
  });

  it('should show skills and responsibilities sections if available', async () => {
    const op = controller.expectOne(GET_JOB);
    op.flush({
      data: {
        job: {
          title: 'Software Engineer',
          summary: null,
          url: null,
          locations: null,
          skills: ['Development', 'Testing'],
          responsibilities: ['Write product or system development code', 'Participate in, or lead design reviews'],
          qualifications: null,
        },
      },
    });

    await fixture.whenStable();

    expect(fixture.debugElement.query(By.directive(NbSpinnerComponent))).toBeTruthy();

    fixture.detectChanges();

    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('h2')?.textContent).toBe('Software Engineer')
    expect(fixture.debugElement.query(By.directive(NbSpinnerComponent))).toBeFalsy();
    const sectionHeaders = Array.from(element.querySelectorAll('h3')).map((heading: HTMLHeadingElement) => heading.textContent);
    expect(sectionHeaders.length).toBe(2);
    expect(sectionHeaders).toContain('Skills');
    expect(sectionHeaders).toContain('Responsibilities');
  })
});
