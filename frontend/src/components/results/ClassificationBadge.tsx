'use client';

import { Box, Chip, Typography } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';

interface ClassificationBadgeProps {
  label: 'Original' | 'Fake';
  confidence: number;
}

export default function ClassificationBadge({ label, confidence }: ClassificationBadgeProps) {
  const isOriginal = label === 'Original';

  return (
    <Box sx={{ textAlign: 'center', py: 3 }}>
      <Chip
        icon={isOriginal ? <CheckCircleIcon /> : <WarningIcon />}
        label={label}
        color={isOriginal ? 'success' : 'error'}
        sx={{
          fontSize: '1.5rem',
          py: 3,
          px: 2,
          height: 'auto',
          '& .MuiChip-label': {
            px: 2,
          },
          '& .MuiChip-icon': {
            fontSize: '2rem',
          },
        }}
      />

      <Typography variant="h6" sx={{ mt: 2 }} color="text.secondary">
        Confidence: {(confidence * 100).toFixed(1)}%
      </Typography>
    </Box>
  );
}
