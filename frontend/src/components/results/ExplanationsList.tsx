'use client';

import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

interface ExplanationsListProps {
  explanations: string[];
}

export default function ExplanationsList({ explanations }: ExplanationsListProps) {
  if (!explanations || explanations.length === 0) {
    return null;
  }

  return (
    <Paper elevation={2} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Analysis Details
      </Typography>

      <List>
        {explanations.map((explanation, index) => (
          <ListItem key={index} alignItems="flex-start">
            <ListItemIcon>
              <InfoIcon color="primary" />
            </ListItemIcon>
            <ListItemText
              primary={explanation}
              primaryTypographyProps={{
                variant: 'body1',
              }}
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}
