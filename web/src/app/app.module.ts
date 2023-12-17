import { NgModule } from '@angular/core';
import { BrowserModule, provideProtractorTestingSupport } from '@angular/platform-browser';
import { provideRouter, RouterModule, RouterOutlet } from '@angular/router';
import { NbLayoutModule, NbThemeModule } from '@nebular/theme';
import { NbEvaIconsModule } from '@nebular/eva-icons';

import { AppComponent } from './app.component';
import { JobListComponent } from './job-list/job-list.component';
import { routes } from './app.routes';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    RouterOutlet,
    BrowserModule,
    RouterModule.forRoot([]),
    NbThemeModule.forRoot({ name: 'dark'}),
    NbLayoutModule,
    NbEvaIconsModule,
    JobListComponent,
  ],
  providers: [provideRouter(routes), provideProtractorTestingSupport()],
  bootstrap: [AppComponent]
})
export class AppModule { }
