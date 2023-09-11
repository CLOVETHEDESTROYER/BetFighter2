import Axios, { AxiosError, AxiosResponse } from 'axios';


export const betFighterAPI = Axios.create({
  //mine did :5000 so you might need to change this for what your local api port is, 8000 i assume
  baseURL: "http://localhost:8000/"

});