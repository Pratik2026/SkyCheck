import axios from "axios";
import "../App";

// API Service
export const apiService = {
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",

  async sendMessage(request) {
    try {
      const response = await axios.post(`${this.baseURL}/chat`, request);
      return response.data;
    } catch (error) {
      throw {
        message:
          error.response?.data?.error || error.message || "An error occurred",
        status: error.response?.status,
      };
    }
  },
};
