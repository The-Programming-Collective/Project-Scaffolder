import { Route, Routes } from 'react-router-dom';
import Home from '../pages/Home/Home';

const AppRoutes = () => {
	return (
		<Routes>
			<Route path="/" element={<Home />} />
			{/* Add other routes here */}
		</Routes>
	);
};

export default AppRoutes;
