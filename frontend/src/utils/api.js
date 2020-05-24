import axios from "axios";

// export const backend = axios.create({
//   baseURL: window._env_.REACT_APP_BACKEND_URL,
//   responseType: "json",
// });

export const usersApi = axios.create({
  baseURL: "http://userapi.manvsvirus.lignum.eti.br/v1", // window._env_.REACT_APP_USERAPI_URL,
  responseType: "json"
})

