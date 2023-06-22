import axios from 'axios';

export default async function handler(req, res) {
  try {
    const response = await axios.get('http://localhost:5000/fetch_data');
    const data = response.data.result.rows;
    res.status(200).json(data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to fetch data' });
  }
}