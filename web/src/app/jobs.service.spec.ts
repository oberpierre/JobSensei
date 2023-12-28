import { TestBed } from '@angular/core/testing';

import { JobsService } from './jobs.service';

describe('JobsService', () => {
  let service: JobsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JobsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getJobs', () => {
    it('should return a list of jobs', (done) => {
      service.getJobs().subscribe((jobs) => {
        expect(jobs).toHaveSize(2);
        done();
      });
    })
  })
});
