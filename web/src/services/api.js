import axios from "../node_modules/axios/dist/axios.min.js";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://localhost:8008",
});

export default api;
