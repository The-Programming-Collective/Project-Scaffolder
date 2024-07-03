import API_BASE_URL from '../config/apiConfig';

const api = {
	fetchData: async (endpoint) => {
		const response = await fetch(`${API_BASE_URL}/${endpoint}`);
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const data = await response.json();
		return data;
	},
};

export default api;
