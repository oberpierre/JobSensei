import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NbThemeService, NbIconModule, NbToggleModule } from '@nebular/theme';

export const THEME_KEY = 'theme';
export enum THEME {
  LIGHT = 'light',
  DARK = 'dark',
}

@Component({
  selector: 'app-theme-toggle',
  standalone: true,
  imports: [CommonModule, NbIconModule, NbToggleModule],
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
    const themeSetting = localStorage.getItem(THEME_KEY);
    if (themeSetting !== null) {
      return themeSetting === THEME.LIGHT;
    } else if (window.matchMedia?.('(prefers-color-scheme: light)')?.matches) {
      return true;
    }
    return false;
  }

  themeChange(isLightTheme: boolean, persist = false) {
    this.themeService.changeTheme(isLightTheme ? 'default' : 'dark');
    persist && localStorage.setItem(THEME_KEY, isLightTheme ? THEME.LIGHT : THEME.DARK);
  }
}
