import { counterReducer, initialState } from './counter.reducer';
import * as CounterActions from '../actions/counter.actions';

describe('Counter Reducer', () => {
  it('should return the initial state', () => {
    const action = { type: 'Unknown' };
    const state = counterReducer(undefined, action);

    expect(state).toBe(initialState);
  });

  it('should increment the state', () => {
    const action = CounterActions.increment();
    const state = counterReducer(initialState, action);

    expect(state).toBe(initialState + 1);
  });

  it('should decrement the state', () => {
    const action = CounterActions.decrement();
    const state = counterReducer(initialState, action);

    expect(state).toBe(initialState - 1);
  });
});
