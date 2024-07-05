import * as CounterActions from './counter.actions';

describe('Counter Actions', () => {
  it('should create an increment action', () => {
    const action = CounterActions.increment();
    expect(action.type).toBe('[Counter] Increment');
  });

  it('should create a decrement action', () => {
    const action = CounterActions.decrement();
    expect(action.type).toBe('[Counter] Decrement');
  });
});
