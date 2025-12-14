import axios, { AxiosError } from 'axios';
import type {
  ClassificationResponse,
  FeedbackRequest,
  FeedbackResponse,
  HealthResponse,
  StatsResponse,
  ApiError,
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Error handler
const handleApiError = (error: AxiosError): ApiError => {
  if (error.response) {
    return {
      detail: (error.response.data as any)?.detail || 'An error occurred',
      status: error.response.status,
    };
  } else if (error.request) {
    return {
      detail: 'No response from server. Please check your connection.',
      status: 503,
    };
  } else {
    return {
      detail: error.message || 'An unexpected error occurred',
      status: 500,
    };
  }
};

// API Methods
export const api = {
  /**
   * Classify an uploaded image
   */
  async classifyImage(file: File): Promise<ClassificationResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await apiClient.post<ClassificationResponse>(
        '/api/v1/classify',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  /**
   * Submit user feedback
   */
  async submitFeedback(feedback: FeedbackRequest): Promise<FeedbackResponse> {
    try {
      const response = await apiClient.post<FeedbackResponse>(
        '/api/v1/feedback',
        feedback
      );

      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  /**
   * Check API health
   */
  async checkHealth(): Promise<HealthResponse> {
    try {
      const response = await apiClient.get<HealthResponse>('/api/v1/health');
      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  /**
   * Get system statistics
   */
  async getStats(): Promise<StatsResponse> {
    try {
      const response = await apiClient.get<StatsResponse>('/api/v1/stats');
      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },
};

export default api;
