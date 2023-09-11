import axios from 'axios';
import {betFighterAPI} from './axios'

export  async function handler(req, res) {
    const data = await axios.get('http://localhost:8000/');
    console.log(data)
    res.status(200).json(data.data);
  }
  
export default function Home({ data }) {
    return (
      <div>
        <h1>Data from Flask backend:</h1>
        <p>{JSON.stringify(data)}</p>
      </div>
    );
  }
  export async function getStaticProps() {
    const { data } = await axios.get('http://localhost:8000/');
    return { props: { data } };
  }

  //TODO: added my api call here in this function so you can call it easily from your pages, and in different spots if needed.
  export async function testMonica(){
    //I put it in a promise so that you can deal with the response/errors
    return new Promise((resolve, reject) => {
    //We set the baseURL in axios.tsx, that way all you need to do is add the call type (GET, POST, PUT) and the endpoint route. This is good if you want to change the url at some point when you actually deploy it somewhere, then you only need to change it in one place.
    betFighterAPI.get('/mk').then((response:any) => {
        console.log('in the response promise', response)
        resolve(response.data)})
      .catch((err: any) => reject(err));
  });  
}

export async function winnerResponse() {
  try {
    const response = await betFighterAPI.get('/mk');
    console.log('in the response promise', response)
    return response.data;
  } catch (error) {
    throw error;
  }
}



  
  export async function testSecondFunctionMonica(){
    return new Promise((resolve, reject) => {
    betFighterAPI.get('/testroute').then((response:any) => {
        console.log('in the response promise', response)
        resolve(response.data)})
      .catch((err: any) => reject(err));
  });  
}

