import { useState, useEffect } from 'react';
import { Box, Container, Typography } from '@mui/material';
import Grid from '@mui/material/Unstable_Grid2';
import StatsCard from '../components/StatsCard';
import ActivityFeed from '../components/ActivityFeed';
import BotStatusCard from '../components/BotStatusCard';
import BotControls from '../components/BotControls';
import MentionsManager from '../components/MentionsManager';
import CreatePost from '../components/CreatePost';
import { API_BASE_URL } from '../config';

interface Stats {
  total_interactions: number;
  successful_replies: number;
  average_response_time: string;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [activities, setActivities] = useState([]);
  const [botStatus, setBotStatus] = useState(null);
  const [isBotActive, setIsBotActive] = useState(false);

  useEffect(() => {
    // Fetch initial data
    fetchDashboardData();
    // Set up polling every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, activitiesRes, statusRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/stats`),
        fetch(`${API_BASE_URL}/api/recent-activities`),
        fetch(`${API_BASE_URL}/api/bot-status`)
      ]);

      const [statsData, activitiesData, statusData] = await Promise.all([
        statsRes.json(),
        activitiesRes.json(),
        statusRes.json()
      ]);

      setStats(statsData);
      setActivities(activitiesData.activities);
      setBotStatus(statusData);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const handleStartBot = async () => {
    try {
      await fetch(`${API_BASE_URL}/api/bot/start`, { method: 'POST' });
      setIsBotActive(true);
    } catch (error) {
      console.error('Error starting bot:', error);
    }
  };

  const handleStopBot = async () => {
    try {
      await fetch(`${API_BASE_URL}/api/bot/stop`, { method: 'POST' });
      setIsBotActive(false);
    } catch (error) {
      console.error('Error stopping bot:', error);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Twitter Bot Dashboard
      </Typography>
      
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={3}>
          <Grid xs={12}>
            <CreatePost />
          </Grid>
          <Grid xs={12} md={4}>
            <BotControls 
              isActive={isBotActive}
              onStart={handleStartBot}
              onStop={handleStopBot}
            />
          </Grid>
          {/* Bot Status */}
          <Grid xs={12} md={4}>
            <BotStatusCard status={botStatus} />
          </Grid>

          {/* Key Metrics */}
          <Grid xs={12} md={8}>
            <Box sx={{ width: '100%' }}>
              <Grid container spacing={2}>
                <Grid xs={12} sm={6}>
                  <StatsCard 
                    title="Total Interactions"
                    value={stats?.total_interactions || 0}
                    icon="chat"
                  />
                </Grid>
                <Grid xs={12} sm={6}>
                  <StatsCard 
                    title="Success Rate"
                    value={stats ? `${(stats.successful_replies / stats.total_interactions * 100).toFixed(1)}%` : '0%'}
                    icon="check_circle"
                  />
                </Grid>
              </Grid>
            </Box>
          </Grid>

          {/* Recent Activity Feed */}
          <Grid xs={12}>
            <ActivityFeed activities={activities} />
          </Grid>

          <Grid xs={12}>
            <MentionsManager />
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}