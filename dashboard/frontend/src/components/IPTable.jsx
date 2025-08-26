import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Chip,
  Typography,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import { Block, CheckCircle } from '@mui/icons-material';

const IPTable = () => {
  const [blockedIPs, setBlockedIPs] = useState([]);
  const [topAttackers, setTopAttackers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [blockDialogOpen, setBlockDialogOpen] = useState(false);
  const [newBlockIP, setNewBlockIP] = useState('');
  const [blockReason, setBlockReason] = useState('');

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [blockedResponse, attackersResponse] = await Promise.all([
        fetch('http://localhost:5000/api/blocked-ips'),
        fetch('http://localhost:5000/api/top-attackers?limit=20')
      ]);
      
      const blockedData = await blockedResponse.json();
      const attackersData = await attackersResponse.json();
      
      setBlockedIPs(blockedData);
      setTopAttackers(attackersData);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch IP data:', error);
      setLoading(false);
    }
  };

  const handleUnblock = async (ipAddress) => {
    try {
      const response = await fetch('http://localhost:5000/api/unblock-ip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ip_address: ipAddress }),
      });
      
      if (response.ok) {
        fetchData(); // Refresh data
      }
    } catch (error) {
      console.error('Failed to unblock IP:', error);
    }
  };

  const handleBlock = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/block-ip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          ip_address: newBlockIP, 
          reason: blockReason || 'Manual block'
        }),
      });
      
      if (response.ok) {
        setBlockDialogOpen(false);
        setNewBlockIP('');
        setBlockReason('');
        fetchData(); // Refresh data
      }
    } catch (error) {
      console.error('Failed to block IP:', error);
    }
  };

  const isBlocked = (ipAddress) => {
    return blockedIPs.some(blocked => blocked.ip_address === ipAddress);
  };

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">IP Management</Typography>
        <Button
          variant="contained"
          color="error"
          startIcon={<Block />}
          onClick={() => setBlockDialogOpen(true)}
        >
          Block IP
        </Button>
      </Box>

      {/* Blocked IPs Table */}
      <Typography variant="h6" gutterBottom>
        Currently Blocked IPs ({blockedIPs.length})
      </Typography>
      <TableContainer component={Paper} sx={{ mb: 4 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>IP Address</TableCell>
              <TableCell>Blocked At</TableCell>
              <TableCell>Reason</TableCell>
              <TableCell>Expires At</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {blockedIPs.map((blocked, index) => (
              <TableRow key={index}>
                <TableCell>
                  <Typography variant="body2" fontFamily="monospace">
                    {blocked.ip_address}
                  </Typography>
                </TableCell>
                <TableCell>
                  {new Date(blocked.blocked_at).toLocaleString()}
                </TableCell>
                <TableCell>{blocked.reason}</TableCell>
                <TableCell>
                  {blocked.expires_at ? new Date(blocked.expires_at).toLocaleString() : 'Never'}
                </TableCell>
                <TableCell>
                  <Button
                    size="small"
                    color="success"
                    startIcon={<CheckCircle />}
                    onClick={() => handleUnblock(blocked.ip_address)}
                  >
                    Unblock
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Top Attackers Table */}
      <Typography variant="h6" gutterBottom>
        Top Attackers (Last 24h)
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>IP Address</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Attack Count</TableCell>
              <TableCell>Services</TableCell>
              <TableCell>Last Attack</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {topAttackers.map((attacker, index) => (
              <TableRow key={index}>
                <TableCell>
                  <Typography variant="body2" fontFamily="monospace">
                    {attacker.ip_address}
                  </Typography>
                </TableCell>
                <TableCell>
                  {attacker.city}, {attacker.country}
                </TableCell>
                <TableCell>
                  <Chip 
                    label={attacker.attack_count} 
                    color={attacker.attack_count > 10 ? 'error' : attacker.attack_count > 5 ? 'warning' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {attacker.services?.split(',').map(service => (
                    <Chip key={service} label={service.toUpperCase()} size="small" sx={{ mr: 0.5 }} />
                  ))}
                </TableCell>
                <TableCell>
                  {new Date(attacker.last_attack).toLocaleString()}
                </TableCell>
                <TableCell>
                  {isBlocked(attacker.ip_address) ? (
                    <Chip label="Blocked" color="error" size="small" />
                  ) : (
                    <Chip label="Active" color="warning" size="small" />
                  )}
                </TableCell>
                <TableCell>
                  {!isBlocked(attacker.ip_address) && (
                    <Button
                      size="small"
                      color="error"
                      startIcon={<Block />}
                      onClick={() => {
                        setNewBlockIP(attacker.ip_address);
                        setBlockReason(`High attack count: ${attacker.attack_count} attacks`);
                        setBlockDialogOpen(true);
                      }}
                    >
                      Block
                    </Button>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Block IP Dialog */}
      <Dialog open={blockDialogOpen} onClose={() => setBlockDialogOpen(false)}>
        <DialogTitle>Block IP Address</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="IP Address"
            fullWidth
            variant="outlined"
            value={newBlockIP}
            onChange={(e) => setNewBlockIP(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Reason"
            fullWidth
            variant="outlined"
            value={blockReason}
            onChange={(e) => setBlockReason(e.target.value)}
            multiline
            rows={2}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBlockDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleBlock} variant="contained" color="error">
            Block IP
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default IPTable;
