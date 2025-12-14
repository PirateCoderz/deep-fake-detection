'use client';

import { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Alert,
  ButtonGroup,
} from '@mui/material';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import { useFeedback } from '@/hooks/useFeedback';

interface FeedbackFormProps {
  requestId: string;
}

export default function FeedbackForm({ requestId }: FeedbackFormProps) {
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [comments, setComments] = useState('');
  const { submitFeedback, loading, error, success } = useFeedback();

  const handleSubmit = async () => {
    if (isCorrect === null) return;

    await submitFeedback({
      request_id: requestId,
      is_correct: isCorrect,
      comments: comments.trim() || undefined,
    });
  };

  if (success) {
    return (
      <Paper elevation={2} sx={{ p: 3 }}>
        <Alert severity="success">
          Thank you for your feedback! It helps improve our system.
        </Alert>
      </Paper>
    );
  }

  return (
    <Paper elevation={2} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Was this classification correct?
      </Typography>

      <ButtonGroup fullWidth sx={{ mb: 2 }}>
        <Button
          variant={isCorrect === true ? 'contained' : 'outlined'}
          color="success"
          startIcon={<ThumbUpIcon />}
          onClick={() => setIsCorrect(true)}
          disabled={loading}
        >
          Correct
        </Button>
        <Button
          variant={isCorrect === false ? 'contained' : 'outlined'}
          color="error"
          startIcon={<ThumbDownIcon />}
          onClick={() => setIsCorrect(false)}
          disabled={loading}
        >
          Incorrect
        </Button>
      </ButtonGroup>

      <TextField
        fullWidth
        multiline
        rows={3}
        label="Comments (optional)"
        value={comments}
        onChange={(e) => setComments(e.target.value)}
        disabled={loading}
        sx={{ mb: 2 }}
      />

      <Button
        fullWidth
        variant="contained"
        onClick={handleSubmit}
        disabled={isCorrect === null || loading}
      >
        {loading ? 'Submitting...' : 'Submit Feedback'}
      </Button>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error.detail}
        </Alert>
      )}
    </Paper>
  );
}
