'use client';

import { Box, Typography, CircularProgress } from '@mui/material';

interface ConfidenceScoreProps {
  confidence: number;
  label: 'Original' | 'Fake';
}

export default function ConfidenceScore({ confidence, label }: ConfidenceScoreProps) {
  const percentage = confidence * 100;
  const color = confidence >= 0.8 ? 'success' : confidence >= 0.6 ? 'warning' : 'error';

  return (
    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
      <CircularProgress
        variant="determinate"
        value={percentage}
        size={120}
        thickness={4}
        color={color}
      />
      <Box
        sx={{
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
          position: 'absolute',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
        }}
      >
        <Typography variant="h4" component="div" fontWeight="bold">
          {percentage.toFixed(0)}%
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {label}
        </Typography>
      </Box>
    </Box>
  );
}
