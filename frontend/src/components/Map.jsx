import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import 'maplibre-gl/dist/maplibre-gl.css';

import * as maplibregl from 'maplibre-gl';
import { Protocol } from 'pmtiles';
import { maplibreGL } from '@maplibre/maplibre-gl-leaflet';
import maplibreWorker from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';
import styles from '@/components/Map.module.scss';
import { API_URL, toApiYear } from '@/components/Constants.jsx';

maplibregl.setWorkerUrl(maplibreWorker);
const protocol = new Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

function CensusTiles({ censusYear, geoLevel }) {
  const map = useMap();
  const maplibreLayerRef = useRef(null);

  // 1. Ensure a dedicated pane exists above the base tile layer
  useEffect(() => {
    if (!map.getPane('vectorPane')) {
      const pane = map.createPane('vectorPane');
      // Leaflet's base tilePane has zIndex 200, overlayPane has 400
      pane.style.zIndex = '450';
      pane.style.pointerEvents = 'none'; // Allows clicks to pass through to map if needed
    }
  }, [map]);

  useEffect(() => {
    if (!censusYear || !geoLevel || geoLevel === 'auto') return;

    let isMounted = true;
    const apiYear = toApiYear(censusYear);

    async function loadTiles() {
      try {
        const params = new URLSearchParams({
          census_year: apiYear,
          geo_level: geoLevel,
        });

        const res = await fetch(`${API_URL}/api/vector_tiles?${params}`);
        if (!res.ok) return;

        const data = await res.json();
        if (!isMounted) return;

        if (maplibreLayerRef.current) {
          map.removeLayer(maplibreLayerRef.current);
          maplibreLayerRef.current = null;
        }

        const layer = maplibreGL({
          // 2. Explicitly bind the layer to our high z-index pane
          pane: 'vectorPane',
          style: {
            version: 8,
            sources: {
              census: {
                type: 'vector',
                url: `pmtiles://${API_URL}${data.url}`,
                promoteId: apiYear === 2021 ? 'DGUID' : 'GEO_CODE',
                minzoom: 0,
                maxzoom: 14,
              },
            },
            layers: [
              {
                id: 'census-fill',
                type: 'fill',
                source: 'census',
                'source-layer': data.source_layer,
                paint: {
                  'fill-color': '#3388ff',
                  'fill-opacity': 0.5,
                },
              },
              {
                id: 'census-outline',
                type: 'line',
                source: 'census',
                'source-layer': data.source_layer,
                paint: {
                  'line-color': '#333',
                  'line-width': 1,
                },
              },
            ],
          },
        });

        if (!isMounted) return;

        maplibreLayerRef.current = layer;
        layer.addTo(map);

      } catch (err) {
        console.error('Error loading vector layer:', err);
      }
    }

    loadTiles();

    return () => {
      isMounted = false;
      if (maplibreLayerRef.current && map.hasLayer(maplibreLayerRef.current)) {
        map.removeLayer(maplibreLayerRef.current);
        maplibreLayerRef.current = null;
      }
    };
  }, [map, censusYear, geoLevel]);

  return null;
}

export default function Map({ censusYear, geoLevel }) {
  const position = [56.1304, -98.5795];

  return (
    <MapContainer
      center={position}
      zoom={4}
      scrollWheelZoom={true}
      className={styles.mapBox}
    >
      <TileLayer
        attribution='&copy; OpenStreetMap | Statistics Canada'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <CensusTiles censusYear={censusYear} geoLevel={geoLevel} />
    </MapContainer>
  );
}