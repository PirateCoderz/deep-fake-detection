'use client';

import { useState } from 'react';
import { api } from '@/services/api';
import type { ClassificationResponse, ApiError } from '@/types';

interface UseClassificationReturn {
  classify: (file: File) => Promise<ClassificationResponse | null>;
  loading: boolean;
  error: ApiError | null;
  result: ClassificationResponse | null;
  reset: () => void;
}

export function useClassification(): UseClassificationReturn {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [result, setResult] = useState<ClassificationResponse | null>(null);

  const classify = async (file: File): Promise<ClassificationResponse | null> => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await api.classifyImage(file);
      setResult(response);
      return response;
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setLoading(false);
    setError(null);
    setResult(null);
  };

  return {
    classify,
    loading,
    error,
    result,
    reset,
  };
}
