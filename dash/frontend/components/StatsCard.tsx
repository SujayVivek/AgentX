import { Card, CardContent, Typography, Box } from '@mui/material';
import Icon from '@mui/material/Icon';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: string;
}

export default function StatsCard({ title, value, icon }: StatsCardProps) {
  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography color="textSecondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h5" component="div">
              {value}
            </Typography>
          </Box>
          <Icon color="primary" fontSize="large">{icon}</Icon>
        </Box>
      </CardContent>
    </Card>
  );
}
