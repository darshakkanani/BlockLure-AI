import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import { Dashboard, Security, Map, Timeline, Block, Search } from '@mui/icons-material';

// Import components
import DashboardView from './components/Dashboard';
import AttackMap from './components/GeoMap';
import AttackChart from './components/AttackChart';
import IPTable from './components/IPTable';
import LiveFeed from './components/LiveFeed';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00bcd4',
    },
    secondary: {
      main: '#ff5722',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
});

const drawerWidth = 240;

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/stats');
      const data = await response.json();
      setStats(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
      setLoading(false);
    }
  };

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <Dashboard /> },
    { id: 'map', label: 'Attack Map', icon: <Map /> },
    { id: 'timeline', label: 'Timeline', icon: <Timeline /> },
    { id: 'blocked', label: 'Blocked IPs', icon: <Block /> },
    { id: 'search', label: 'Search', icon: <Search /> },
  ];

  const renderContent = () => {
    switch (currentView) {
      case 'dashboard':
        return <DashboardView stats={stats} />;
      case 'map':
        return <AttackMap />;
      case 'timeline':
        return <AttackChart />;
      case 'blocked':
        return <IPTable />;
      case 'search':
        return <LiveFeed />;
      default:
        return <DashboardView stats={stats} />;
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex' }}>
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <Security sx={{ mr: 2 }} />
            <Typography variant="h6" noWrap component="div">
              BlockLure-AI Dashboard
            </Typography>
            <Box sx={{ flexGrow: 1 }} />
            <Typography variant="body2">
              {loading ? 'Loading...' : `${stats.total_attacks || 0} Total Attacks`}
            </Typography>
          </Toolbar>
        </AppBar>

        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          <Toolbar />
          <Box sx={{ overflow: 'auto' }}>
            <List>
              {menuItems.map((item) => (
                <ListItem
                  button
                  key={item.id}
                  selected={currentView === item.id}
                  onClick={() => setCurrentView(item.id)}
                >
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.label} />
                </ListItem>
              ))}
            </List>
          </Box>
        </Drawer>

        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          {renderContent()}
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
