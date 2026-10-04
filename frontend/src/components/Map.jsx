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

function OpenFreeMapLayer() {
  const map = useMap();
  const layerRef = useRef(null);

  useEffect(() => {
    if (!map.getPane('vectorPane')) {
      const pane = map.createPane('vectorPane');
      pane.style.zIndex = '450';
      pane.style.pointerEvents = 'none';
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

function getColour(value, min, max, numColours = 3) {
  const lightest = [247, 251, 255];
  const darkest = [8, 48, 107];

  if (min === max) {
    return darkest;
  }

  const width = (max - min) / numColours;

  let bin = Math.floor((value - min) / width);

  // pd.cut() has a maximum bin at the upper boundary.
  bin = Math.min(bin, numColours - 1);

  return lightest.map((start, i) => {
    const end = darkest[i];

    return Math.round(
      start + ((end - start) * bin) / (numColours - 1),
    );
  });
}

function CensusTiles({
  censusYear,
  geoLevel,
  charId,
  value,
}) {
  const map = useMap();

  const maplibreLayerRef = useRef(null);
  const valueCache = useRef(new Map());

  useEffect(() => {
    if (!censusYear || !geoLevel || geoLevel === 'auto') {
      return;
    }

    if (charId == null || value == null) {
      return;
    }

    let isMounted = true;
    let mapLibreMap = null;

    const apiYear = toApiYear(censusYear);

    async function updateVisibleValues() {
      if (!mapLibreMap) return;

      const features = mapLibreMap.queryRenderedFeatures({
        layers: ['census-fill'],
      });

      const geoCodes = [
        ...new Set(
          features
            .map(feature => feature.id)
            .filter(
              id => id !== undefined && id !== null,
            )
            .map(String),
        ),
      ];

      if (geoCodes.length === 0) return;

      const missingGeoCodes = geoCodes.filter(
        geoCode => !valueCache.current.has(geoCode),
      );

      if (missingGeoCodes.length > 0) {
        const response = await fetch(
          `${API_URL}/api/population_batch`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              census_year: apiYear,
              geo_codes: missingGeoCodes,
              char_id: charId,
              value,
            }),
          },
        );

        if (!response.ok) {
          console.error(
            'Population request failed:',
            response.status,
          );
          return;
        }

        const data = await response.json();

        for (const item of data) {
          valueCache.current.set(
            String(item.geo_code),
            item.value,
          );
        }
      }

      const visibleValues = geoCodes
        .map(geoCode => valueCache.current.get(geoCode))
        .filter(
          currentValue =>
            currentValue !== null &&
            currentValue !== undefined &&
            Number.isFinite(Number(currentValue)),
        );

      if (visibleValues.length === 0) return;

      const min = Math.min(...visibleValues);
      const max = Math.max(...visibleValues);

      const expression = [
        'case',
      ];

      for (const geoCode of geoCodes) {
        const currentValue =
          valueCache.current.get(geoCode);

        if (
          currentValue === null ||
          currentValue === undefined ||
          !Number.isFinite(Number(currentValue))
        ) {
          continue;
        }

        const colour = getColour(
          Number(currentValue),
          min,
          max,
        );

        expression.push(
          ['==', ['id'], geoCode],
          `rgb(${colour[0]}, ${colour[1]}, ${colour[2]})`,
        );
      }

      expression.push('#cccccc');

      mapLibreMap.setPaintProperty(
        'census-fill',
        'fill-color',
        expression,
      );
    }

    async function loadTiles() {
      try {
        const params = new URLSearchParams({
          census_year: apiYear,
          geo_level: geoLevel,
        });

        const res = await fetch(
          `${API_URL}/api/vector_tiles?${params}`,
        );

        if (!res.ok) return;

        const data = await res.json();

        if (!isMounted) return;

        if (maplibreLayerRef.current) {
          map.removeLayer(
            maplibreLayerRef.current,
          );
          maplibreLayerRef.current = null;
        }

        const layer = maplibreGL({
          pane: 'vectorPane',

          style: {
            version: 8,

            sources: {
              census: {
                type: 'vector',
                url: `pmtiles://${API_URL}${data.url}`,
                promoteId:
                  apiYear === 2021
                    ? 'DGUID'
                    : 'GEO_CODE',
                minzoom: 0,
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
                  'fill-opacity': 0.75,
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

        maplibreLayerRef.current = layer;
        layer.addTo(map);

        mapLibreMap = layer.getMaplibreMap();

        mapLibreMap.once('idle', () => {
          if (isMounted) {
            updateVisibleValues();
          }
        });

        mapLibreMap.on(
          'moveend',
          updateVisibleValues,
        );
      } catch (err) {
        console.error(
          'Error loading vector layer:',
          err,
        );
      }
    }

    valueCache.current.clear();

    loadTiles();

    return () => {
      isMounted = false;

      if (mapLibreMap) {
        mapLibreMap.off(
          'moveend',
          updateVisibleValues,
        );
      }

      if (
        maplibreLayerRef.current &&
        map.hasLayer(maplibreLayerRef.current)
      ) {
        map.removeLayer(
          maplibreLayerRef.current,
        );

        maplibreLayerRef.current = null;
      }
    };
  }, [
    map,
    censusYear,
    geoLevel,
    charId,
    value,
  ]);

  return null;
}

export default function CensusMap({ 
  censusYear,
  geoLevel,
  charId,
  value,
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
        value={value}
      />
    </MapContainer>
  );
}