import axios from 'axios';


const fetchData = async () => {
  try {
    const response = await axios.get('/api');
    const data = response.data;
    console.log(data);
  } catch (error) {
    console.error(error);
  }
};