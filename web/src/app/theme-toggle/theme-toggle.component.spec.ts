import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ThemeToggleComponent } from './theme-toggle.component';
import { NbLayoutDirectionService, NbStatusService, NbThemeService, NbToggleComponent } from '@nebular/theme';
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
  let nbThemeServiceSpy: jasmine.SpyObj<NbThemeService>;

  beforeEach(async () => {
    nbThemeServiceSpy = jasmine.createSpyObj(NbThemeService, ['changeTheme']);
    await TestBed.configureTestingModule({
      imports: [NoopAnimationsModule, ThemeToggleComponent],
      providers: [
        {provide: NbLayoutDirectionService, useClass: MockNbLayoutDirectionService},
        {provide: NbStatusService, useClass: MockNbStatusService},
        {provide: NbThemeService, useValue: nbThemeServiceSpy},
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

  it('should change the theme upon toggling', async () => {
    const toggle = fixture.nativeElement.querySelector('input');
    
    expect(toggle?.checked).toBe(false);

    toggle?.click();
    expect(toggle?.checked).toBe(true);
    expect(nbThemeServiceSpy.changeTheme).toHaveBeenCalledTimes(1);
    expect(nbThemeServiceSpy.changeTheme.calls.argsFor(0)).toEqual(['default']);

    toggle?.click();
    expect(toggle?.checked).toBe(false);
    expect(nbThemeServiceSpy.changeTheme).toHaveBeenCalledTimes(2);
    expect(nbThemeServiceSpy.changeTheme.calls.argsFor(1)).toEqual(['dark']);
  })
});
