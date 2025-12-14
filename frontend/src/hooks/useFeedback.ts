'use client';

import { useState } from 'react';
import { api } from '@/services/api';
import type { FeedbackRequest, FeedbackResponse, ApiError } from '@/types';

interface UseFeedbackReturn {
  submitFeedback: (feedback: FeedbackRequest) => Promise<boolean>;
  loading: boolean;
  error: ApiError | null;
  success: boolean;
  reset: () => void;
}

export function useFeedback(): UseFeedbackReturn {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [success, setSuccess] = useState(false);

  const submitFeedback = async (feedback: FeedbackRequest): Promise<boolean> => {
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      await api.submitFeedback(feedback);
      setSuccess(true);
      return true;
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setLoading(false);
    setError(null);
    setSuccess(false);
  };

  return {
    submitFeedback,
    loading,
    error,
    success,
    reset,
  };
}
