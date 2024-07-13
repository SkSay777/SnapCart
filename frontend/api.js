import axios from 'axios';

const API_URL = 'http://your-flask-app-url'; // Replace with your Flask app URL

export const getRecommendations = async (prod, nbr) => {
  try {
    const response = await axios.post(`${API_URL}/recommendations`, {
      prod,
      nbr,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations', error);
    throw error;
  }
};
