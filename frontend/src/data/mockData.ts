import type { ClassificationResponse, StatsResponse } from '@/types';

export const mockClassificationResult: ClassificationResponse = {
  request_id: 'mock-123-456-789',
  label: 'Original',
  confidence: 0.92,
  probabilities: {
    Original: 0.92,
    Fake: 0.08,
  },
  heatmap_available: true,
  explanations: [
    'Logo shows clear, high-quality printing consistent with authentic products',
    'Print quality indicates professional manufacturing',
    'All visual indicators strongly suggest authentic packaging',
  ],
  low_confidence_warning: false,
  processing_time_ms: 245.5,
};

export const mockLowConfidenceResult: ClassificationResponse = {
  request_id: 'mock-low-conf-123',
  label: 'Fake',
  confidence: 0.55,
  probabilities: {
    Original: 0.45,
    Fake: 0.55,
  },
  heatmap_available: true,
  explanations: [
    'Print quality appears inconsistent with authentic products',
    'Some visual indicators suggest potential counterfeit',
    'Further verification recommended',
  ],
  low_confidence_warning: true,
  processing_time_ms: 312.8,
};

export const mockStats: StatsResponse = {
  total_classifications: 1247,
  accuracy_estimate: 0.89,
  average_confidence: 0.84,
  category_distribution: {
    original: 823,
    fake: 424,
  },
  feedback_count: 456,
};

export const mockExplanations = {
  original: [
    'Logo shows clear, high-quality printing consistent with authentic products',
    'Print quality indicates professional manufacturing',
    'Color consistency matches authentic product standards',
    'All visual indicators strongly suggest authentic packaging',
    'Texture and material quality align with genuine products',
  ],
  fake: [
    'Print quality appears inconsistent with authentic products',
    'Logo clarity is below expected standards',
    'Color deviation detected from authentic product samples',
    'Texture analysis suggests non-standard materials',
    'Visual indicators suggest potential counterfeit',
  ],
};
