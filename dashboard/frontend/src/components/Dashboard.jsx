import React, { useState, useEffect } from 'react';
import { Grid, Card, CardContent, Typography, Box, CircularProgress } from '@mui/material';
import { Security, Warning, Block, Public } from '@mui/icons-material';
import AttackChart from './AttackChart';
import GeoMap from './GeoMap';

const StatCard = ({ title, value, icon, color = 'primary' }) => (
  <Card>
    <CardContent>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Box>
          <Typography color="textSecondary" gutterBottom variant="body2">
            {title}
          </Typography>
          <Typography variant="h4" component="h2">
            {value}
          </Typography>
        </Box>
        <Box color={`${color}.main`}>
          {icon}
        </Box>
      </Box>
    </CardContent>
  </Card>
);

const DashboardView = ({ stats }) => {
  const [recentAttacks, setRecentAttacks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecentAttacks();
  }, []);

  const fetchRecentAttacks = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/attacks?limit=10');
      const data = await response.json();
      setRecentAttacks(data.attacks || []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch recent attacks:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Security Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Attacks"
            value={stats.total_attacks || 0}
            icon={<Security fontSize="large" />}
            color="primary"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Recent Attacks (24h)"
            value={stats.recent_attacks || 0}
            icon={<Warning fontSize="large" />}
            color="warning"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Blocked IPs"
            value={stats.blocked_ips || 0}
            icon={<Block fontSize="large" />}
            color="error"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Unique IPs"
            value={stats.unique_ips || 0}
            icon={<Public fontSize="large" />}
            color="info"
          />
        </Grid>

        {/* Attack Timeline Chart */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Attack Timeline (24h)
              </Typography>
              <AttackChart />
            </CardContent>
          </Card>
        </Grid>

        {/* Top Services */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top Targeted Services
              </Typography>
              {stats.top_services?.map((service, index) => (
                <Box key={service.service} display="flex" justifyContent="space-between" mb={1}>
                  <Typography variant="body2">{service.service.toUpperCase()}</Typography>
                  <Typography variant="body2" color="primary">
                    {service.count}
                  </Typography>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Geographic Map */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Attack Origins (Geographic)
              </Typography>
              <Box height="400px">
                <GeoMap />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Attacks Feed */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Attacks
              </Typography>
              <Box maxHeight="300px" overflow="auto">
                {recentAttacks.map((attack, index) => (
                  <Box key={index} p={1} borderBottom="1px solid #333">
                    <Typography variant="body2" color="primary">
                      {attack.service?.toUpperCase()} - {attack.ip_address}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {attack.country} | {new Date(attack.timestamp).toLocaleString()}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardView;
