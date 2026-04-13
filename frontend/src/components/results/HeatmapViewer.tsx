'use client';

import {
    Box,
    Paper,
    Typography,
    Chip,
} from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';

interface HeatmapViewerProps {
    heatmapBase64: string | null;
    heatmapAvailable: boolean;
    label: string;
}

export default function HeatmapViewer({ heatmapBase64, heatmapAvailable, label }: HeatmapViewerProps) {
    if (!heatmapAvailable || !heatmapBase64) {
        return null;
    }

    return (
        <Paper elevation={2} sx={{ p: 3, mt: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <VisibilityIcon color="primary" />
                <Typography variant="h6">
                    Grad-CAM Visual Explanation
                </Typography>
            </Box>

            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                The heatmap highlights regions the AI focused on to make its decision.
                {label === 'Fake'
                    ? ' Red/warm areas indicate suspicious regions that suggest the product may be counterfeit.'
                    : ' Red/warm areas indicate regions that confirm the product appears authentic.'}
            </Typography>

            <Box
                sx={{
                    position: 'relative',
                    width: '100%',
                    maxWidth: 400,
                    mx: 'auto',
                    borderRadius: 2,
                    overflow: 'hidden',
                    border: '2px solid',
                    borderColor: label === 'Fake' ? 'error.main' : 'success.main',
                }}
            >
                <img
                    src={`data:image/png;base64,${heatmapBase64}`}
                    alt="Grad-CAM heatmap overlay showing AI focus areas"
                    style={{
                        width: '100%',
                        height: 'auto',
                        display: 'block',
                    }}
                />
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, mt: 2 }}>
                <Chip
                    size="small"
                    label="Cool (blue) = Low attention"
                    sx={{ bgcolor: '#3b82f6', color: 'white', fontSize: '0.7rem' }}
                />
                <Chip
                    size="small"
                    label="Warm (red) = High attention"
                    sx={{ bgcolor: '#ef4444', color: 'white', fontSize: '0.7rem' }}
                />
            </Box>
        </Paper>
    );
}
