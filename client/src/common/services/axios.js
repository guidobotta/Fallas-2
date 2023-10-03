import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://localhost:8080",
});

// axiosInstance.interceptors.request.use(request => {
//   console.log("Starting Request", JSON.stringify(request, null, 2))
//   return request
// })

// axiosInstance.interceptors.response.use(response => {
//   console.log("Response:", JSON.stringify(response, null, 2))
//   return response
// })

export default axiosInstance;