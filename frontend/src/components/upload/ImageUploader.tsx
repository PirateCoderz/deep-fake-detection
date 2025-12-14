'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Paper,
  Typography,
  Button,
  Alert,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import ImageIcon from '@mui/icons-material/Image';
import { validateImageFile } from '@/utils/validation';
import type { UploadedFile } from '@/types';

interface ImageUploaderProps {
  onFileSelect: (file: UploadedFile) => void;
  disabled?: boolean;
}

export default function ImageUploader({ onFileSelect, disabled = false }: ImageUploaderProps) {
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      setError(null);

      if (acceptedFiles.length === 0) {
        setError('No file selected');
        return;
      }

      const file = acceptedFiles[0];
      const validation = validateImageFile(file);

      if (!validation.valid) {
        setError(validation.error || 'Invalid file');
        return;
      }

      // Create preview URL
      const preview = URL.createObjectURL(file);

      onFileSelect({ file, preview });
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/heic': ['.heic'],
    },
    multiple: false,
    disabled,
  });

  return (
    <Box>
      <Paper
        {...getRootProps()}
        elevation={3}
        sx={{
          p: 4,
          textAlign: 'center',
          cursor: disabled ? 'not-allowed' : 'pointer',
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.300',
          bgcolor: isDragActive ? 'action.hover' : 'background.paper',
          transition: 'all 0.3s',
          '&:hover': {
            borderColor: disabled ? 'grey.300' : 'primary.main',
            bgcolor: disabled ? 'background.paper' : 'action.hover',
          },
        }}
      >
        <input {...getInputProps()} />

        <CloudUploadIcon
          sx={{
            fontSize: 64,
            color: isDragActive ? 'primary.main' : 'grey.400',
            mb: 2,
          }}
        />

        <Typography variant="h6" gutterBottom>
          {isDragActive ? 'Drop the image here' : 'Drag & drop an image here'}
        </Typography>

        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          or
        </Typography>

        <Button
          variant="contained"
          startIcon={<ImageIcon />}
          disabled={disabled}
        >
          Browse Files
        </Button>

        <Typography variant="caption" display="block" sx={{ mt: 2 }} color="text.secondary">
          Supported formats: JPEG, PNG, HEIC (Max 10MB)
        </Typography>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
}
