import React, { useState, useEffect } from 'react';
import { Box, Button, TextField, Card, Typography, Grid } from '@mui/material';
import { API_BASE_URL } from '../config';

interface Mention {
  id: string;
  text: string;
  author: string;
  created_at: string;
}

export default function MentionsManager() {
  const [mentions, setMentions] = useState<Mention[]>([]);
  const [selectedMention, setSelectedMention] = useState<string | null>(null);
  const [generatedReply, setGeneratedReply] = useState<string>('');
  const [customPrompt, setCustomPrompt] = useState<string>('');

  const fetchMentions = async () => {
    const response = await fetch(`${API_BASE_URL}/api/mentions`);
    const data = await response.json();
    setMentions(data);
  };

  const generateReply = async (mentionId: string, prompt?: string) => {
    const response = await fetch(`${API_BASE_URL}/api/generate-reply`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mention_id: mentionId, custom_prompt: prompt }),
    });
    const data = await response.json();
    setGeneratedReply(data.reply);
  };

  const postReply = async (mentionId: string) => {
    await fetch('/api/post-reply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mention_id: mentionId }),
    });
    setSelectedMention(null);
    setGeneratedReply('');
    fetchMentions();
  };

  useEffect(() => {
    const interval = setInterval(fetchMentions, 30000);
    fetchMentions();
    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Pending Mentions</Typography>
      
      <Grid container spacing={3}>
        {mentions.map((mention) => (
          <Grid item xs={12} key={mention.id}>
            <Card sx={{ p: 2 }}>
              <Typography><strong>@{mention.author}:</strong> {mention.text}</Typography>
              <Box sx={{ mt: 2 }}>
                <Button 
                  variant="contained" 
                  onClick={() => {
                    setSelectedMention(mention.id);
                    generateReply(mention.id);
                  }}
                >
                  Generate Reply
                </Button>
              </Box>

              {selectedMention === mention.id && (
                <Box sx={{ mt: 2 }}>
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    value={generatedReply}
                    label="Generated Reply"
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                    label="Custom Instructions (Optional)"
                    margin="normal"
                  />
                  <Box sx={{ mt: 2 }}>
                    <Button 
                      variant="contained" 
                      color="primary"
                      onClick={() => postReply(mention.id)}
                      sx={{ mr: 1 }}
                    >
                      Confirm & Post
                    </Button>
                    <Button 
                      variant="contained"
                      onClick={() => generateReply(mention.id)}
                      sx={{ mr: 1 }}
                    >
                      Regenerate
                    </Button>
                    <Button 
                      variant="contained"
                      onClick={() => generateReply(mention.id, customPrompt)}
                    >
                      Generate with Custom Instructions
                    </Button>
                  </Box>
                </Box>
              )}
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
} 