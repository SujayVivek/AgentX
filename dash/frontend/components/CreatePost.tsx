import React, { useState } from 'react';
import { 
  Box, 
  Button, 
  TextField, 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions,
  Typography,
  CircularProgress
} from '@mui/material';
import { API_BASE_URL } from '../config';

export default function CreatePost() {
  const [open, setOpen] = useState(false);
  const [prompt, setPrompt] = useState<string>('');
  const [generatedPost, setGeneratedPost] = useState<string>('');
  const [editedPost, setEditedPost] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [isPosting, setIsPosting] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
    setPrompt('');
    setGeneratedPost('');
    setEditedPost('');
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-tweet`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error: ${errorText}`);
      }
      
      const data = await response.json();
      setGeneratedPost(data.post);
      setEditedPost(data.post);
    } catch (error) {
      console.error('Error details:', error);
      setError(error instanceof Error ? error.message : 'Failed to generate post');
    } finally {
      setIsGenerating(false);
    }
  };

  const handlePost = async () => {
    if (!editedPost.trim()) return;
    
    setIsPosting(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/post`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: editedPost })
      });
      
      if (response.ok) {
        handleClose();
      }
    } catch (error) {
      console.error('Error posting:', error);
    } finally {
      setIsPosting(false);
    }
  };

  return (
    <>
      <Button 
        variant="contained" 
        color="primary" 
        onClick={handleOpen}
        sx={{ mb: 2 }}
      >
        Create New Post
      </Button>

      <Dialog 
        open={open} 
        onClose={handleClose}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Create New Post</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            {error && (
              <Typography color="error" sx={{ mb: 2 }}>
                {error}
              </Typography>
            )}
            <TextField
              fullWidth
              label="What kind of post would you like to create?"
              multiline
              rows={2}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="E.g., Write a tweet about the latest developments in AI"
              disabled={isGenerating}
            />
            
            <Button
              variant="contained"
              onClick={handleGenerate}
              disabled={!prompt.trim() || isGenerating}
              sx={{ mt: 2 }}
            >
              {isGenerating ? (
                <>
                  <CircularProgress size={24} sx={{ mr: 1 }} />
                  Generating...
                </>
              ) : 'Generate Post'}
            </Button>

            {generatedPost && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Generated Post:
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  value={editedPost}
                  onChange={(e) => setEditedPost(e.target.value)}
                  placeholder="Edit the generated post here..."
                />
              </Box>
            )}
          </Box>
        </DialogContent>
        
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button 
            onClick={handlePost}
            variant="contained"
            disabled={!editedPost.trim() || isPosting}
          >
            {isPosting ? (
              <>
                <CircularProgress size={24} sx={{ mr: 1 }} />
                Posting...
              </>
            ) : 'Post'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
} 