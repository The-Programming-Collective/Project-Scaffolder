import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement } from '../redux/slices/counterSlice';

const useCounter = () => {
	const count = useSelector((state) => state.counter.value);
	const dispatch = useDispatch();

	const incrementCount = () => dispatch(increment());
	const decrementCount = () => dispatch(decrement());

	return { count, incrementCount, decrementCount };
};

export default useCounter;
