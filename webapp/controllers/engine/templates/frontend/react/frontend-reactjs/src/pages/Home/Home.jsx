import React, { useEffect, useState } from 'react';
import './Home.css';
import Counter from '../../components/common/Counter/Counter';
import ReactLogo from '../../assets/logos/logo.svg';
import ScaffolderLogo from '../../assets/logos/Scaffolder.svg';
import api from '../../services/api';

const Home = () => {
	const [data, setData] = useState({ title: 'Backend: Nodejs & PostgreSQL' });
	const [error, setError] = useState(null);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const result = await api.fetchData('api/v1');
				setData(result);
			} catch (err) {
				setError(err.message);
			}
		};

		fetchData();
	}, []);

	return (
		<div className="home">
			<header className="home-header">
				<img
					src={ScaffolderLogo}
					className="scaffolder-logo"
					alt="scaffolder logo"
				/>
				<img src={ReactLogo} className="react-logo" alt="react logo" />
			</header>
			<p>
				<span>{error ? error : data.title}</span> Happy coding 🚀
			</p>
			<Counter />
		</div>
	);
};

export default Home;
