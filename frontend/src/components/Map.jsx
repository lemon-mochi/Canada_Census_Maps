import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import styles from '@/components/Map.module.scss';

// Fix for default marker icons missing in production builds (optional but recommended)
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

export default function Map() {
  // Coordinates for the center of the map [Latitude, Longitude]
  const position = [56.1304, -98.5795]; //centre of Canada

  return (
    <MapContainer
        center={position}
        zoom={4}
        scrollWheelZoom={true}
        className={styles.mapBox}
    >
      {/* TileLayer provides the map graphic. Using OpenStreetMap here */}
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
    </MapContainer>
  );
}
