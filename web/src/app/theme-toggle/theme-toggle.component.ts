import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NbToggleModule } from '@nebular/theme';

@Component({
  selector: 'app-theme-toggle',
  standalone: true,
  imports: [CommonModule, NbToggleModule],
  templateUrl: './theme-toggle.component.html',
  styleUrl: './theme-toggle.component.css'
})
export class ThemeToggleComponent {
}
