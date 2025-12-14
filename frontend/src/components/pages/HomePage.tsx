'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Container,
  Box,
  Typography,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ImageUploader from '@/components/upload/ImageUploader';
import ImagePreview from '@/components/upload/ImagePreview';
import { useClassification } from '@/hooks/useClassification';
import type { UploadedFile } from '@/types';

export default function HomePage() {
  const router = useRouter();
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const { classify, loading, error } = useClassification();

  const handleFileSelect = (file: UploadedFile) => {
    setUploadedFile(file);
  };

  const handleRemoveFile = () => {
    if (uploadedFile) {
      URL.revokeObjectURL(uploadedFile.preview);
    }
    setUploadedFile(null);
  };

  const handleClassify = async () => {
    if (!uploadedFile) return;

    const result = await classify(uploadedFile.file);

    if (result) {
      // Store result in sessionStorage for results page
      sessionStorage.setItem('classificationResult', JSON.stringify(result));
      sessionStorage.setItem('uploadedImage', uploadedFile.preview);

      // Navigate to results page
      router.push(`/results/${result.request_id}`);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 8 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
          Fake Product Detection
        </Typography>
        <Typography variant="h6" color="text.secondary" paragraph>
          AI-powered product authenticity verification
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Upload an image of a product to verify its authenticity
        </Typography>
      </Box>

      {!uploadedFile ? (
        <ImageUploader onFileSelect={handleFileSelect} disabled={loading} />
      ) : (
        <Box>
          <ImagePreview
            file={uploadedFile.file}
            preview={uploadedFile.preview}
            onRemove={handleRemoveFile}
          />

          <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              variant="outlined"
              onClick={handleRemoveFile}
              disabled={loading}
            >
              Change Image
            </Button>
            <Button
              variant="contained"
              size="large"
              onClick={handleClassify}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : <CheckCircleIcon />}
            >
              {loading ? 'Analyzing...' : 'Verify Authenticity'}
            </Button>
          </Box>
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mt: 3 }}>
          {error.detail}
        </Alert>
      )}

      {loading && (
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <CircularProgress />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Analyzing image... This may take a few moments
          </Typography>
        </Box>
      )}
    </Container>
  );
}
