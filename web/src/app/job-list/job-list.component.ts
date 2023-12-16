import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NbCardModule, NbListModule } from '@nebular/theme';
import { JobCardComponent } from '../job-card/job-card.component';
import { Job } from '../job';

@Component({
  selector: 'app-job-list',
  standalone: true,
  imports: [
    CommonModule,
    NbCardModule,
    NbListModule,
    JobCardComponent,
  ],
  templateUrl: './job-list.component.html',
  styleUrl: './job-list.component.css'
})
export class JobListComponent {
  jobs: Job[] = [{
    title: "Software Engineer, Machine Learning",
    summary: "Google is seeking a Software Engineer to develop the next-generation technologies that change how billions of users connect, explore, and interact with information and one another. The ideal candidate will have experience in software development, data structures or algorithms, ML algorithms/tools (e.g., TensorFlow), AI, deep learning, or natural language processing.",
  }, {
    title: "Student Researcher",
    summary: "Google is looking for a Student Researcher to work on critical research projects and collaborate with Google's research scientists and engineers.",
  }]
}
