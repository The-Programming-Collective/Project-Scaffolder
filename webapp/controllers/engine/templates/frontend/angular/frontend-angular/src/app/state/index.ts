import { ActionReducerMap } from '@ngrx/store';
import { AppState } from './app.state';
import { counterReducer } from './reducers/counter.reducer';

export const reducers: ActionReducerMap<AppState> = {
  counter: counterReducer,
};
