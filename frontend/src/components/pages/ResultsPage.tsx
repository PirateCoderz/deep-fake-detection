'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Container,
  Box,
  Typography,
  Button,
  Grid,
  Paper,
  Alert,
} from '@mui/material';
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import WarningIcon from '@mui/icons-material/Warning';
import Image from 'next/image';
import ClassificationBadge from '@/components/results/ClassificationBadge';
import ConfidenceScore from '@/components/results/ConfidenceScore';
import ExplanationsList from '@/components/results/ExplanationsList';
import FeedbackForm from '@/components/results/FeedbackForm';
import type { ClassificationResponse } from '@/types';

interface ResultsPageProps {
  requestId: string;
}

export default function ResultsPage({ requestId }: ResultsPageProps) {
  const router = useRouter();
  const [result, setResult] = useState<ClassificationResponse | null>(null);
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);

  useEffect(() => {
    // Get result from sessionStorage
    const storedResult = sessionStorage.getItem('classificationResult');
    const storedImage = sessionStorage.getItem('uploadedImage');

    if (storedResult) {
      setResult(JSON.parse(storedResult));
    }

    if (storedImage) {
      setUploadedImage(storedImage);
    }
  }, []);

  const handleBackToHome = () => {
    // Clean up sessionStorage
    sessionStorage.removeItem('classificationResult');
    sessionStorage.removeItem('uploadedImage');
    router.push('/');
  };

  if (!result) {
    return (
      <Container maxWidth="md" sx={{ py: 8 }}>
        <Alert severity="info">
          No classification result found. Please upload an image first.
        </Alert>
        <Button
          variant="contained"
          onClick={handleBackToHome}
          sx={{ mt: 2 }}
        >
          Go to Upload
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Button
        startIcon={<ArrowBackIosIcon />}
        onClick={handleBackToHome}
        sx={{ mb: 3 }}
      >
        Back to Upload
      </Button>

      <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
        Classification Results
      </Typography>

      {result.low_confidence_warning && (
        <Alert severity="warning" icon={<WarningIcon />} sx={{ mb: 3 }}>
          Low confidence detected. The classification may not be reliable. Consider
          uploading a clearer image or seeking additional verification.
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Left Column - Image and Badge */}
        <Grid item xs={12} md={6}>
          {uploadedImage && (
            <Paper elevation={3} sx={{ p: 2, mb: 3 }}>
              <Box
                sx={{
                  position: 'relative',
                  width: '100%',
                  height: 400,
                  borderRadius: 1,
                  overflow: 'hidden',
                }}
              >
                <Image
                  src={uploadedImage}
                  alt="Uploaded product"
                  fill
                  style={{ objectFit: 'contain' }}
                />
              </Box>
            </Paper>
          )}

          <ClassificationBadge
            label={result.label}
            confidence={result.confidence}
          />

          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
            <ConfidenceScore
              confidence={result.confidence}
              label={result.label}
            />
          </Box>

          <Paper elevation={2} sx={{ p: 2, mt: 3 }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Request ID:</strong> {result.request_id}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <strong>Processing Time:</strong> {result.processing_time_ms.toFixed(0)}ms
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <strong>Probabilities:</strong>
            </Typography>
            <Box sx={{ pl: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Original: {(result.probabilities.Original * 100).toFixed(1)}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Fake: {(result.probabilities.Fake * 100).toFixed(1)}%
              </Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Right Column - Explanations and Feedback */}
        <Grid item xs={12} md={6}>
          <ExplanationsList explanations={result.explanations} />

          <Box sx={{ mt: 3 }}>
            <FeedbackForm requestId={result.request_id} />
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
}
