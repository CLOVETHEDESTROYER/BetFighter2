import { betFighterAPI } from './axios';

export async function handler(req, res) {
  try {
    const { data } = await betFighterAPI.get('/mk');
    console.log(data);
    res.status(200).json(data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
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
  try {
    const { data } = await betFighterAPI.get('/mk');
    return { props: { data } };
  } catch (error) {
    console.error(error);
    return { props: { data: null } };
  }
}

export async function winnerResponse() {
  return new Promise((resolve, reject) => {
    betFighterAPI
      .get('/mk')
      .then((response: any) => {
        console.log('in the response promise', response);
        resolve(response.data);
      })
      .catch((err: any) => reject(err));
  });
}

export async function testSecondFunctionMonica() {
  return new Promise((resolve, reject) => {
    betFighterAPI
      .get('/testroute')
      .then((response: any) => {
        console.log('in the response promise', response);
        resolve(response.data);
      })
      .catch((err: any) => reject(err));
  });
}
