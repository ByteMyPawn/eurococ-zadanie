import axios from "axios";

const api = axios.create({
    baseURL: "http://api:8000", // Názov služby v docker-compose.yml
});


export default api;
