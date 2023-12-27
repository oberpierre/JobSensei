import { Injectable } from '@angular/core';
import { Job } from './job';

@Injectable({
  providedIn: 'root'
})
export class JobsService {

  constructor() {}

  getJobs(): Job[] {
    return [{
      uuid: "1",
      title: "Software Engineer, Machine Learning",
      summary: "Google is seeking a Software Engineer to develop the next-generation technologies that change how billions of users connect, explore, and interact with information and one another. The ideal candidate will have experience in software development, data structures or algorithms, ML algorithms/tools (e.g., TensorFlow), AI, deep learning, or natural language processing.",
    }, {
      uuid: "2",
      title: "Student Researcher",
      summary: "Google is looking for a Student Researcher to work on critical research projects and collaborate with Google's research scientists and engineers.",
    }];
  }
}
