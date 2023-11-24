# JobSensei Angular Frontend

This is the frontend for the JobSensei project, it shows the user the jobs and offers an admin dashboard. It was generated with [Angular CLI](https://github.com/angular/angular-cli) version 16.2.8 and set up to follow more idiomatic approach by having Bazel managing the dependencies and using the Angular `ngc` compiler directly for the build process. Also refer to [Bazel Example Angular NGC](https://github.com/aspect-build/bazel-examples/tree/main/angular-ngc), which was refered to when setting up the project.

## Development server

Run `ibazel run //web/src:serve` to run a dev server. Navigate to `http://localhost:8080/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `bazel build //web/...` to build the project.

## Running unit tests

Run `bazel test //web/...` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.
For any issues or questions related to this Bazel-integrated setup, refer to the Angular NGC example mentioned above.
