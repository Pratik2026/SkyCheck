import axios from "axios";
import "../App";

export const apiService = {
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",

  async sendMessage(request) {
    try {
      const response = await axios.post(`${this.baseURL}/chat`, request, {
        timeout: 30000,
      });

      if (
        response.data.success &&
        response.data.response &&
        (response.data.response.startsWith("⚠") ||
          response.data.response
            .toLowerCase()
            .includes("error occurred during processing"))
      ) {
        let errorMessage = "An error occurred while processing your request";

        const responseText = response.data.response;
        if (responseText.includes("API key not valid")) {
          errorMessage = "Service configuration error - please try again later";
        } else if (responseText.includes("timeout")) {
          errorMessage = "Request timeout - please try again";
        } else if (
          responseText.includes("rate limit") ||
          responseText.includes("quota")
        ) {
          errorMessage = "Service is busy - please try again in a moment";
        } else if (responseText.includes("authentication")) {
          errorMessage =
            "Authentication error - service temporarily unavailable";
        }

        throw {
          message: errorMessage,
          status: 500,
          isBackendError: true,
        };
      }

      return response.data;
    } catch (error) {
      if (error.isBackendError) {
        throw error;
      }

      let errorMessage = "An unexpected error occurred";
      let errorCode = "UNKNOWN_ERROR";

      if (error.code === "ECONNABORTED") {
        errorMessage = "Request timeout - please try again";
        errorCode = "TIMEOUT_ERROR";
      } else if (error.response) {
        const { status, data } = error.response;

        if (data && data.detail) {
          if (typeof data.detail === "object" && data.detail.error) {
            errorMessage = data.detail.error;
            errorCode = data.detail.code || "SERVER_ERROR";
          } else if (typeof data.detail === "string") {
            errorMessage = data.detail;
          }
        } else if (status >= 500) {
          errorMessage = "Server error - please try again later";
          errorCode = "SERVER_ERROR";
        } else if (status === 429) {
          errorMessage = "Too many requests - please wait a moment";
          errorCode = "RATE_LIMIT_ERROR";
        } else if (status === 401) {
          errorMessage =
            "Authentication error - service temporarily unavailable";
          errorCode = "AUTH_ERROR";
        } else if (status === 408) {
          errorMessage = "Request timeout - please try again";
          errorCode = "TIMEOUT_ERROR";
        } else if (status === 400) {
          errorMessage = data?.error || "Invalid request";
          errorCode = "BAD_REQUEST";
        } else {
          errorMessage = `HTTP ${status} error`;
          errorCode = "HTTP_ERROR";
        }
      } else if (error.request) {
        // Network error
        errorMessage = "Network error - please check your connection";
        errorCode = "NETWORK_ERROR";
      }

      throw {
        message: errorMessage,
        status: error.response?.status,
        code: errorCode,
        originalError: error,
      };
    }
  },
};
