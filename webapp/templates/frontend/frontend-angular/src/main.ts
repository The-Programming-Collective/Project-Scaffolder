import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideRouter } from '@angular/router';
import { provideStore } from '@ngrx/store';
import { provideEffects } from '@ngrx/effects';
import { provideStoreDevtools } from '@ngrx/store-devtools';

import { appRoutes } from './app/app.routes';
import { reducers } from './app/state';
import { provideHttpClient } from '@angular/common/http';

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(appRoutes),
    provideStore(reducers),
    provideEffects([]),
    provideHttpClient(),
    provideStoreDevtools({ maxAge: 25, logOnly: false }),
  ],
}).catch((err) => console.error(err));
