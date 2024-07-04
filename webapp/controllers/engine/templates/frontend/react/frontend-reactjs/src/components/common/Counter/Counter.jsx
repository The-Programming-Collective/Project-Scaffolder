import React from 'react';
import './Counter.css';
import useCounter from '../../../hooks/useCounter';

const Counter = () => {
	const { count, incrementCount, decrementCount } = useCounter();

	return (
		<div className="counter">
			<h1>{count}</h1>
			<button onClick={decrementCount}>Decrement</button>
			<button onClick={incrementCount}>Increment</button>
		</div>
	);
};

export default Counter;
