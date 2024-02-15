import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ThemeToggleComponent } from './theme-toggle.component';
import { NbLayoutDirectionService, NbStatusService } from '@nebular/theme';
import { of } from 'rxjs';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

class MockNbLayoutDirectionService {
  onDirectionChange = () => {
    return of();
  }
  isLtr = () => true
}
class MockNbStatusService {
  isCustomStatus = () => false;
}

describe('ThemeToggleComponent', () => {
  let component: ThemeToggleComponent;
  let fixture: ComponentFixture<ThemeToggleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NoopAnimationsModule, ThemeToggleComponent],
      providers: [
        {provide: NbLayoutDirectionService, useClass: MockNbLayoutDirectionService},
        {provide: NbStatusService, useClass: MockNbStatusService},
      ]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ThemeToggleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create theme toggle', () => {
    expect(component).toBeTruthy();
  });
});
