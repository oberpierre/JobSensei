import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NbBadgeModule, NbListModule } from '@nebular/theme';
import { Job } from '../job';

@Component({
  selector: 'app-job-card',
  standalone: true,
  imports: [
    NbBadgeModule,
    NbListModule,
    CommonModule,
  ],
  templateUrl: './job-card.component.html',
  styleUrl: './job-card.component.css'
})
export class JobCardComponent {
  @Input() job: Job = {uuid: '', title: ''};
}
