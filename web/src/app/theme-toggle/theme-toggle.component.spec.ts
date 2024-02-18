import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ThemeToggleComponent, THEME_KEY } from './theme-toggle.component';
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
    localStorage.clear();
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
  });

  it('should create theme toggle', () => {
    fixture.detectChanges();

    expect(component).toBeTruthy();
  });

  it('should change the theme upon toggling and persist changes', async () => {
    spyOn(component, 'getThemeSetting').and.returnValue(false);
    fixture.detectChanges();
    const toggle = fixture.nativeElement.querySelector('input');
    
    expect(toggle?.checked).toBe(false);
    expect(component.checked).toBe(false);
    expect(localStorage.getItem(THEME_KEY)).toBe(null);
    expect(nbThemeServiceSpy.changeTheme).toHaveBeenCalledTimes(1);
    expect(nbThemeServiceSpy.changeTheme.calls.argsFor(0)).toEqual(['dark']);

    toggle?.click();
    expect(toggle?.checked).toBe(true);
    expect(component.checked).toBe(true);
    expect(localStorage.getItem(THEME_KEY)).toBe('light');
    expect(nbThemeServiceSpy.changeTheme).toHaveBeenCalledTimes(2);
    expect(nbThemeServiceSpy.changeTheme.calls.argsFor(1)).toEqual(['default']);

    toggle?.click();
    expect(toggle?.checked).toBe(false);
    expect(component.checked).toBe(false);
    expect(localStorage.getItem(THEME_KEY)).toBe('dark');
    expect(nbThemeServiceSpy.changeTheme).toHaveBeenCalledTimes(3);
    expect(nbThemeServiceSpy.changeTheme.calls.argsFor(2)).toEqual(['dark']);
  });

  [{theme: 'light', value: true}, {theme: 'dark', value: false}].forEach(({theme, value}) => {
    it(`should initialize toggle with ${value} for system theme ${theme} without persisting`, () => {
      spyOn(window, 'matchMedia').withArgs('(prefers-color-scheme: light)').and.returnValue({matches: value} as MediaQueryList);
      fixture.detectChanges();

      const toggle = fixture.nativeElement.querySelector('input');

      expect(toggle?.checked).toBe(value);
      expect(nbThemeServiceSpy.changeTheme).toHaveBeenCalledTimes(1);
      expect(nbThemeServiceSpy.changeTheme.calls.argsFor(0)).toEqual([theme === 'light' ? 'default' : theme]);
      expect(localStorage.getItem(THEME_KEY)).toBe(null);
    });
  });
});
