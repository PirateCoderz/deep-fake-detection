// API Response Types
export interface ClassificationResponse {
  request_id: string;
  label: 'Original' | 'Fake';
  confidence: number;
  probabilities: {
    Original: number;
    Fake: number;
  };
  heatmap_available: boolean;
  explanations: string[];
  low_confidence_warning: boolean;
  processing_time_ms: number;
}

export interface FeedbackRequest {
  request_id: string;
  is_correct: boolean;
  user_label?: string;
  comments?: string;
}

export interface FeedbackResponse {
  message: string;
  feedback_id: number;
  flagged_for_review: boolean;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  database_connected: boolean;
  redis_available: boolean;
  version: string;
}

export interface StatsResponse {
  total_classifications: number;
  accuracy_estimate: number | null;
  average_confidence: number;
  category_distribution: {
    original: number;
    fake: number;
  };
  feedback_count: number;
}

// Component Props Types
export interface UploadedFile {
  file: File;
  preview: string;
}

export interface ClassificationResult extends ClassificationResponse {
  uploadedImage?: string;
}

// Error Types
export interface ApiError {
  detail: string;
  status?: number;
}
