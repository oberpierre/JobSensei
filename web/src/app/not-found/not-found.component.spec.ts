import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NotFoundComponent } from './not-found.component';

describe('NotFoundComponent', () => {
  let component: NotFoundComponent;
  let fixture: ComponentFixture<NotFoundComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NotFoundComponent],
    })
    .compileComponents()
    .then(() => {
      fixture = TestBed.createComponent(NotFoundComponent);
      component = fixture.componentInstance;
      fixture.detectChanges();
    });
  });

  it('should create NotFound component', () => {
    expect(component).toBeTruthy();
  });

  it('should show page not found', () => {
    const notFoundElement = fixture.nativeElement;
    expect(notFoundElement.textContent).toBe('Page Not Found!');
  })
});
