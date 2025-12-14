'use client';

import { Box, Paper, Typography, IconButton, Chip } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import Image from 'next/image';
import { formatFileSize } from '@/utils/validation';

interface ImagePreviewProps {
  file: File;
  preview: string;
  onRemove: () => void;
}

export default function ImagePreview({ file, preview, onRemove }: ImagePreviewProps) {
  return (
    <Paper elevation={3} sx={{ p: 2, position: 'relative' }}>
      <IconButton
        onClick={onRemove}
        sx={{
          position: 'absolute',
          top: 8,
          right: 8,
          bgcolor: 'background.paper',
          '&:hover': {
            bgcolor: 'error.light',
            color: 'white',
          },
        }}
        size="small"
      >
        <CloseIcon />
      </IconButton>

      <Box
        sx={{
          position: 'relative',
          width: '100%',
          height: 300,
          mb: 2,
          borderRadius: 1,
          overflow: 'hidden',
        }}
      >
        <Image
          src={preview}
          alt="Preview"
          fill
          style={{ objectFit: 'contain' }}
        />
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="body2" noWrap sx={{ flex: 1, mr: 2 }}>
          {file.name}
        </Typography>
        <Chip label={formatFileSize(file.size)} size="small" />
      </Box>
    </Paper>
  );
}
