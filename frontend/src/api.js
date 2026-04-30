import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api/v1",
});

export const generate = (data) => API.post("/generate/", data);
export const getHistory = () => API.get("/history/");
export const getAnalytics = () => API.get("/analytics/");