import { useEffect, useRef } from 'react';
import { MapContainer, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import 'maplibre-gl/dist/maplibre-gl.css';

import * as maplibregl from 'maplibre-gl';
import { Protocol } from 'pmtiles';
import { maplibreGL } from '@maplibre/maplibre-gl-leaflet';
import maplibreWorker from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';
import styles from '@/components/Map.module.scss';
import CensusTiles from '@/components/CensusTiles.jsx';


maplibregl.setWorkerUrl(maplibreWorker);
const protocol = new Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

function OpenFreeMapLayer() {
  const map = useMap();
  const layerRef = useRef(null);

  useEffect(() => {
    if (!map.getPane('vectorPane')) {
      const pane = map.createPane('vectorPane');
      pane.style.zIndex = '450';
      pane.style.pointerEvents = 'auto';
    }
  }, [map]);

  useEffect(() => {
    const layer = maplibreGL({
      style: 'https://tiles.openfreemap.org/styles/positron',
    });

    layerRef.current = layer;
    layer.addTo(map);

    return () => {
      if (layerRef.current && map.hasLayer(layerRef.current)) {
        map.removeLayer(layerRef.current);
        layerRef.current = null;
      }
    };
  }, [map]);

  return null;
}

export default function CensusMap({ 
  censusYear,
  geoLevel,
  charId,
  charName,
  value,
  colourCount,
  equalWidth,
}) {
  const position = [56.1304, -98.5795];

  return (
    <MapContainer
      center={position}
      zoom={4}
      scrollWheelZoom={true}
      className={styles.mapBox}
    >
      <OpenFreeMapLayer />

      <CensusTiles
        censusYear={censusYear}
        geoLevel={geoLevel}
        charId={charId}
        charName={charName}
        value={value}
        colourCount={colourCount}
        equalWidth={equalWidth}
      />
    </MapContainer>
  );
}