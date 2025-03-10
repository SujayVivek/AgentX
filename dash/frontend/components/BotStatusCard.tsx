import { Card, CardContent, Typography, Box, Switch } from '@mui/material';
import { formatDistanceToNow } from 'date-fns';

interface BotStatus {
  is_active: boolean;
  rate_limit_remaining: number;
  rate_limit_reset: string;
}

export default function BotStatusCard({ status }: { status: BotStatus | null }) {
  if (!status) return null;

  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">Bot Status</Typography>
          <Switch
            checked={status.is_active}
            color="primary"
            disabled
          />
        </Box>
        <Box mt={2}>
          <Typography color="textSecondary">
            Rate Limit Remaining: {status.rate_limit_remaining}
          </Typography>
          <Typography color="textSecondary">
            Reset in: {formatDistanceToNow(new Date(status.rate_limit_reset))}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}