import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NbThemeService, NbToggleModule } from '@nebular/theme';

@Component({
  selector: 'app-theme-toggle',
  standalone: true,
  imports: [CommonModule, NbToggleModule],
  templateUrl: './theme-toggle.component.html',
  styleUrl: './theme-toggle.component.css'
})
export class ThemeToggleComponent {
  checked: boolean = false;

  constructor(private themeService: NbThemeService) {}

  
  ngOnInit(): void {
    this.checked = this.getThemeSetting();
    this.themeChange(this.checked);
  }

  getThemeSetting(): boolean {
    if (window.matchMedia?.('(prefers-color-scheme: light)')?.matches) {
      return true;
    }
    return false;
  }

  themeChange(isLightTheme: boolean) {
    this.themeService.changeTheme(isLightTheme ? 'default' : 'dark');
  }
}
