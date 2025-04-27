// axiosInstance.ts
import axios from "axios";
import { refreshAccessToken } from "./utils";
import { useRouter } from "next/navigation"; // For Next.js 13+

const API_URL = 'http://127.0.0.1:8000/api';

const axiosInstance = axios.create({
  baseURL: API_URL,
});

// Request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If 401 and not a refresh request or retried request
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshed = await refreshAccessToken();
        if (refreshed.success) {
          // Update the header and retry the original request
          axios.defaults.headers.common["Authorization"] = `Bearer ${refreshed.access_token}`;
          originalRequest.headers["Authorization"] = `Bearer ${refreshed.access_token}`;
          return axiosInstance(originalRequest);
        }
      } catch (refreshError) {
        // If refresh fails, clear storage and redirect to login
        localStorage.clear();
        window.location.href = '/Components/Login'; // Full page reload to clear state
        return Promise.reject(refreshError);
      }
    }
    
    // For any other error, just reject it
    return Promise.reject(error);
  }
);

export default axiosInstance;