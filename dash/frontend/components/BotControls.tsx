import React from 'react';
import { Button, Card, CardContent, Typography } from '@mui/material';

interface BotControlsProps {
  isActive: boolean;
  onStart: () => void;
  onStop: () => void;
}

export default function BotControls({ isActive, onStart, onStop }: BotControlsProps) {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Bot Controls</Typography>
        <Button 
          variant="contained" 
          color={isActive ? "error" : "success"}
          onClick={isActive ? onStop : onStart}
        >
          {isActive ? "Stop Bot" : "Start Bot"}
        </Button>
      </CardContent>
    </Card>
  );
}