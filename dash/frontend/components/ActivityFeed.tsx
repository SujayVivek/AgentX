import { 
  Card, 
  CardContent, 
  Typography, 
  List, 
  ListItem, 
  ListItemText,
  ListItemIcon,
  Chip
} from '@mui/material';
import { formatDistanceToNow } from 'date-fns';

interface Activity {
  id: string;
  type: string;
  status: string;
  timestamp: string;
  tweet_id: string;
  response_time: string;
}

export default function ActivityFeed({ activities }: { activities: Activity[] }) {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Recent Activities
        </Typography>
        <List>
          {activities.map((activity) => (
            <ListItem key={activity.id} divider>
              <ListItemIcon>
                {activity.type === 'reply' ? '💬' : '🤖'}
              </ListItemIcon>
              <ListItemText
                primary={`Tweet ${activity.tweet_id}`}
                secondary={`${formatDistanceToNow(new Date(activity.timestamp))} ago`}
              />
              <Chip
                label={activity.status}
                color={activity.status === 'success' ? 'success' : 'error'}
                size="small"
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}