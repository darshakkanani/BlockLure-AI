import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const GeoMap = () => {
  const [attacks, setAttacks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGeoData();
    const interval = setInterval(fetchGeoData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchGeoData = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/attacks/geo?hours=24');
      const data = await response.json();
      setAttacks(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch geo data:', error);
      setLoading(false);
    }
  };

  const getMarkerColor = (attackCount) => {
    if (attackCount >= 10) return '#ff0000'; // Red for high
    if (attackCount >= 5) return '#ff8800'; // Orange for medium
    return '#ffff00'; // Yellow for low
  };

  const getMarkerSize = (attackCount) => {
    return Math.min(Math.max(attackCount * 2, 5), 20);
  };

  if (loading) {
    return <div>Loading map...</div>;
  }

  return (
    <MapContainer
      center={[20, 0]}
      zoom={2}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      
      {attacks.map((attack, index) => (
        <CircleMarker
          key={index}
          center={[attack.latitude, attack.longitude]}
          radius={getMarkerSize(attack.attack_count)}
          fillColor={getMarkerColor(attack.attack_count)}
          color="#000"
          weight={1}
          opacity={0.8}
          fillOpacity={0.6}
        >
          <Popup>
            <div>
              <strong>{attack.ip_address}</strong><br />
              <strong>Location:</strong> {attack.city}, {attack.country}<br />
              <strong>Attacks:</strong> {attack.attack_count}<br />
              <strong>Last Attack:</strong> {new Date(attack.last_attack).toLocaleString()}
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
};

export default GeoMap;
