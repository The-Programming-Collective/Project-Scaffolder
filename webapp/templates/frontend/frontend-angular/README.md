# Getting Started with Scaffolder Angular app 🧑‍💻

This project was generated with Scaffolder and [Angular CLI](https://github.com/angular/angular-cli) version 18.0.7.

## Project Structure

```
public/
src/
├── app/
│   ├── core/
│   │   ├── interceptors/
│   │   ├── guards/
│   │   ├── services/
│   │   ├── core.module.ts
│   │   └── index.ts
│   ├── environments/
│   ├── features/
│   │   └── .../
│   │       ├── components/
│   │       │   └── .../
│   │       ├── pages/
│   │       └── index.ts
│   ├── services/
│   ├── shared/
│   │   ├── components/
│   │   ├── directives/
│   │   ├── pipes/
│   │   ├── shared.module.ts
│   │   └── index.ts
│   ├── state/
│   │   ├── actions/
│   │   ├── reducers/
│   │   ├── effects/
│   │   ├── selectors/
│   │   └── index.ts
│   ├── app.component.css
│   ├── app.component.html
│   ├── app.component.spec.ts
│   ├── app.component.ts
│   ├── app.config.ts
│   ├── app.module.ts
│   ├── app.routes.ts
│   ├── assets/
│   index.html
│   main.ts
│   styles.css
angular.json
package.json
README.md
```

## Prerequisites 💀

- Node.js (v12.x or higher)
- npm (v6.x or higher) or yarn (v1.x or higher)
- Angular CLI (version 12.x or later)

### Features 🤜

- `State Management with NgRx`: The application uses NgRx for state management, providing a robust and scalable way to manage state in large applications.
- `API Integration`: The application includes a service to fetch data from an external API, with error handling and fallback mechanisms.
- `Standalone Components`: Utilizes Angular's standalone component feature to simplify component integration.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
