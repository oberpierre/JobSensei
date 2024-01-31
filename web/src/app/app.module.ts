import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { APOLLO_FLAGS, APOLLO_OPTIONS, ApolloModule } from 'apollo-angular';
import { InMemoryCache } from '@apollo/client/core';
import { HttpLink } from 'apollo-angular/http';
import { BrowserModule, provideProtractorTestingSupport } from '@angular/platform-browser';
import { provideRouter, RouterModule, RouterOutlet } from '@angular/router';
import { NbLayoutModule, NbThemeModule } from '@nebular/theme';
import { NbEvaIconsModule } from '@nebular/eva-icons';

import { AppComponent } from './app.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { JobListComponent } from './job-list/job-list.component';
import { routes } from './app.routes';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    ApolloModule,
    HttpClientModule,
    RouterOutlet,
    BrowserModule,
    RouterModule.forRoot(routes),
    NbThemeModule.forRoot({ name: 'dark'}),
    NbLayoutModule,
    NbEvaIconsModule,
    NotFoundComponent,
    JobListComponent,
  ],
  providers: [
    {
      provide: APOLLO_FLAGS,
      useValue: {
        useInitialLoading: true,
      }
    },
    {
      provide: APOLLO_OPTIONS,
      useFactory(httpLink: HttpLink) {
        return {
          cache: new InMemoryCache(),
          link: httpLink.create({
            uri: '/graphql',
          }),
        }
      },
      deps: [HttpLink],
    },
    provideRouter(routes),
    provideProtractorTestingSupport()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
