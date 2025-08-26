import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  InputAdornment,
  List,
  ListItem,
  ListItemText,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Paper,
} from '@mui/material';
import { Search, Security, Warning } from '@mui/icons-material';

const LiveFeed = () => {
  const [attacks, setAttacks] = useState([]);
  const [filteredAttacks, setFilteredAttacks] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [serviceFilter, setServiceFilter] = useState('');
  const [countryFilter, setCountryFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAttacks();
    const interval = setInterval(fetchAttacks, 10000); // Update every 10 seconds
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    filterAttacks();
  }, [attacks, searchQuery, serviceFilter, countryFilter]);

  const fetchAttacks = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/attacks?limit=100');
      const data = await response.json();
      setAttacks(data.attacks || []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch attacks:', error);
      setLoading(false);
    }
  };

  const filterAttacks = () => {
    let filtered = attacks;

    if (searchQuery) {
      filtered = filtered.filter(attack =>
        attack.ip_address.includes(searchQuery) ||
        attack.country?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        attack.city?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        attack.details?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (serviceFilter) {
      filtered = filtered.filter(attack => attack.service === serviceFilter);
    }

    if (countryFilter) {
      filtered = filtered.filter(attack => attack.country === countryFilter);
    }

    setFilteredAttacks(filtered);
  };

  const getUniqueServices = () => {
    return [...new Set(attacks.map(attack => attack.service))].filter(Boolean);
  };

  const getUniqueCountries = () => {
    return [...new Set(attacks.map(attack => attack.country))].filter(Boolean);
  };

  const getThreatColor = (score) => {
    if (score >= 80) return 'error';
    if (score >= 60) return 'warning';
    if (score >= 40) return 'info';
    return 'default';
  };

  const getThreatLabel = (score) => {
    if (score >= 80) return 'Critical';
    if (score >= 60) return 'High';
    if (score >= 40) return 'Medium';
    return 'Low';
  };

  if (loading) {
    return <Typography>Loading attacks...</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Live Attack Feed & Search
      </Typography>

      {/* Search and Filter Controls */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              placeholder="Search by IP, location, or details..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Service</InputLabel>
              <Select
                value={serviceFilter}
                label="Service"
                onChange={(e) => setServiceFilter(e.target.value)}
              >
                <MenuItem value="">All Services</MenuItem>
                {getUniqueServices().map(service => (
                  <MenuItem key={service} value={service}>
                    {service.toUpperCase()}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Country</InputLabel>
              <Select
                value={countryFilter}
                label="Country"
                onChange={(e) => setCountryFilter(e.target.value)}
              >
                <MenuItem value="">All Countries</MenuItem>
                {getUniqueCountries().map(country => (
                  <MenuItem key={country} value={country}>
                    {country}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {/* Results Summary */}
      <Box mb={2}>
        <Typography variant="h6">
          Showing {filteredAttacks.length} of {attacks.length} attacks
        </Typography>
      </Box>

      {/* Attack Feed */}
      <Card>
        <CardContent>
          <List sx={{ maxHeight: '600px', overflow: 'auto' }}>
            {filteredAttacks.map((attack, index) => (
              <ListItem key={index} divider>
                <ListItemText
                  primary={
                    <Box display="flex" alignItems="center" gap={1}>
                      <Security color="primary" />
                      <Typography variant="body1" fontFamily="monospace">
                        {attack.ip_address}
                      </Typography>
                      <Chip
                        label={attack.service?.toUpperCase()}
                        size="small"
                        color="primary"
                      />
                      {attack.threat_score && (
                        <Chip
                          label={getThreatLabel(attack.threat_score)}
                          size="small"
                          color={getThreatColor(attack.threat_score)}
                        />
                      )}
                      {attack.blocked && (
                        <Chip
                          label="BLOCKED"
                          size="small"
                          color="error"
                          icon={<Warning />}
                        />
                      )}
                    </Box>
                  }
                  secondary={
                    <Box>
                      <Typography variant="body2" color="textSecondary">
                        <strong>Location:</strong> {attack.city}, {attack.country}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        <strong>Time:</strong> {new Date(attack.timestamp).toLocaleString()}
                      </Typography>
                      {attack.attack_type && (
                        <Typography variant="body2" color="textSecondary">
                          <strong>Type:</strong> {attack.attack_type}
                        </Typography>
                      )}
                      {attack.details && (
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                          <strong>Details:</strong> {JSON.stringify(JSON.parse(attack.details || '{}'), null, 2)}
                        </Typography>
                      )}
                    </Box>
                  }
                />
              </ListItem>
            ))}
            {filteredAttacks.length === 0 && (
              <ListItem>
                <ListItemText
                  primary="No attacks found"
                  secondary="Try adjusting your search criteria"
                />
              </ListItem>
            )}
          </List>
        </CardContent>
      </Card>
    </Box>
  );
};

export default LiveFeed;
