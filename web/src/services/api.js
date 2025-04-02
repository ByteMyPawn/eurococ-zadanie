import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8008", // Use localhost for browser access
});

export default api;
