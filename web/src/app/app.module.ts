import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { NbLayoutModule, NbThemeModule } from '@nebular/theme';
import { NbEvaIconsModule } from '@nebular/eva-icons';

import { AppComponent } from './app.component';
import { JobListComponent } from './job-list/job-list.component';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot([], { useHash: true }),
    NbThemeModule.forRoot({ name: 'dark'}),
    NbLayoutModule,
    NbEvaIconsModule,
    JobListComponent,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
