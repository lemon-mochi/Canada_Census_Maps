
import { useEffect, useRef } from 'react';
import { useMap } from 'react-leaflet';
import {
  API_URL,
  toApiYear,
  getColValue,
} from '@/constants/Constants.jsx';
import {
  getPromoteID,
  getGeoCode,
  getTileID,
  NUMBER_VALUE_GEO_LEVELS
} from '@/constants/TileMappings.jsx';
import L from 'leaflet';
import { maplibreGL } from '@maplibre/maplibre-gl-leaflet';
import 'maplibre-gl/dist/maplibre-gl.css';

export default function CensusTiles({
  censusYear,
  geoLevel,
  charId,
  charName,
  value,
  colourCount,
  equalWidth,
  setBoundaries,
}) {
  const map = useMap();

  const maplibreLayerRef = useRef(null);
  const mapLibreMapRef = useRef(null);
  const valueCache = useRef(new Map());
  const popupRef = useRef(null);
  const updateValuesRef = useRef(null);

  // Keep the latest settings available to handlers without
  // reloading the tile layer whenever they change.
  const settingsRef = useRef({});
  settingsRef.current = {
    censusYear,
    geoLevel,
    charId,
    charName,
    value,
    colourCount,
    equalWidth,
    setBoundaries,
  };

  // Effect 1: load and manage vector tiles.
  // Only reload when the year or geographic level changes.
  useEffect(() => {
    if (!censusYear || !geoLevel || geoLevel === 'auto') {
      return;
    }

    let isMounted = true;
    let mapLibreMap = null;
    let layer = null;

    const apiYear = toApiYear(censusYear);

    async function loadTiles() {
      try {
        const params = new URLSearchParams({
          census_year: apiYear,
          geo_level: geoLevel,
        });

        const response = await fetch(
          `${API_URL}/api/vector_tiles?${params}`,
        );

        if (!response.ok) return;

        const tileInfo = await response.json();

        if (!isMounted) return;

        layer = maplibreGL({
          pane: 'vectorPane',
          interactive: true,
          style: {
            version: 8,
            sources: {
              census: {
                type: 'vector',
                url: `pmtiles://${API_URL}${tileInfo.url}`,
                promoteId: getPromoteID(apiYear, geoLevel),
                minzoom: 0,
              },
            },
            layers: [
              {
                id: 'census-fill',
                type: 'fill',
                source: 'census',
                'source-layer': tileInfo.source_layer,
                paint: {
                  'fill-color': '#3388ff',
                  'fill-opacity': 0.95,
                },
              },
              {
                id: 'census-outline',
                type: 'line',
                source: 'census',
                'source-layer': tileInfo.source_layer,
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
        mapLibreMapRef.current = mapLibreMap;

        const canvas = mapLibreMap.getCanvas();
        if (canvas) {
          canvas.style.pointerEvents = 'auto';
        }

        // Fetch and apply values to the currently visible features.
        async function updateVisibleValues() {
          const settings = settingsRef.current;

          if (
            !isMounted ||
            !mapLibreMap ||
            settings.charId == null ||
            settings.value == null
          ) {
            return;
          }

          const features = mapLibreMap.queryRenderedFeatures({
            layers: ['census-fill'],
          });

          const geoCodes = [
            ...new Set(
              features
                .map(feature =>
                  getGeoCode(apiYear, geoLevel, feature),
                )
                .filter(id => id != null)
                .map(String),
            ),
          ];

          if (geoCodes.length === 0) {
            settings.setBoundaries?.([]);
            return;
          }

          const response = await fetch(
            `${API_URL}/api/population_batch`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                census_year: apiYear,
                geo_codes: geoCodes,
                char_id: settings.charId,
                value: settings.value,
                num_colours: settings.colourCount,
                equal_width: settings.equalWidth,
              }),
            },
          );

          if (!response.ok || !isMounted) {
            return;
          }

          const result = await response.json();

          if (!isMounted) return;

          settings.setBoundaries?.(result.boundaries ?? []);

          const expression = ['case'];

          for (const item of result.data ?? []) {
            if (!Array.isArray(item.colour)) continue;

            const tileID = getTileID(
              apiYear,
              geoLevel,
              item.geo_code,
            );

            valueCache.current.set(
              String(tileID),
              item.value,
            );

            const useNumberNotString =
              NUMBER_VALUE_GEO_LEVELS.get(apiYear)?.has(geoLevel) ?? false;

            expression.push(
              [
                '==',
                ['id'],
                useNumberNotString
                  ? Number(tileID)
                  : String(tileID),
              ],
              `rgb(${item.colour.join(', ')})`,
            );
          }

          if (expression.length === 1) return;

          expression.push('#cccccc');

          if (
            isMounted &&
            mapLibreMap.getLayer('census-fill')
          ) {
            mapLibreMap.setPaintProperty(
              'census-fill',
              'fill-color',
              expression,
            );
          }
        }

        updateValuesRef.current = updateVisibleValues;

        function handleFeatureClick(e) {
          const settings = settingsRef.current;

          const point = mapLibreMap.project([
            e.latlng.lng,
            e.latlng.lat,
          ]);

          const features = mapLibreMap.queryRenderedFeatures(
            point,
            { layers: ['census-fill'] },
          );

          if (!features.length) return;

          const properties = features[0].properties;
          const promoteId = getPromoteID(apiYear, geoLevel);

          const actualValue = valueCache.current.get(
            String(properties[promoteId]),
          );

          const popupHtml = `
            <div style="
              max-height: 200px;
              overflow-y: auto;
              font-family: sans-serif;
              font-size: 13px;
            ">
              <h4 style="
                margin: 0 0 8px 0;
                font-size: 14px;
                border-bottom: 1px solid #ccc;
                padding-bottom: 4px;
              ">
                GeoCode: ${properties[promoteId] ?? 'N/A'}
              </h4>
              <div><strong>Census year:</strong> ${apiYear}</div>
              <div><strong>Characteristic:</strong> ${settings.charName ?? 'N/A'}</div>
              <div><strong>Column:</strong> ${
                getColValue(apiYear, settings.value) ?? 'nothing here'
              }</div>
              <div><strong>Value:</strong> ${actualValue ?? 'N/A'}</div>
            </div>
          `;

          popupRef.current?.remove();

          popupRef.current = L.popup()
            .setLatLng(e.latlng)
            .setContent(popupHtml)
            .openOn(map);
        }

        map.on('click', handleFeatureClick);

        mapLibreMap.on('moveend', updateVisibleValues);

        mapLibreMap.once('idle', () => {
          if (isMounted) {
            updateVisibleValues();
          }
        });

        // Store handler for cleanup.
        clickHandlerRef.current = handleFeatureClick;
      } catch (err) {
        console.error('Error loading vector layer:', err);
      }
    }

    valueCache.current.clear();
    loadTiles();

    return () => {
      isMounted = false;

      popupRef.current?.remove();
      popupRef.current = null;

      if (mapLibreMap) {
        mapLibreMap.off(
          'moveend',
          updateValuesRef.current,
        );
      }

      if (clickHandlerRef.current) {
        map.off('click', clickHandlerRef.current);
        clickHandlerRef.current = null;
      }

      if (maplibreLayerRef.current === layer && layer) {
        if (map.hasLayer(layer)) {
          map.removeLayer(layer);
        }

        maplibreLayerRef.current = null;
        mapLibreMapRef.current = null;
      }

      updateValuesRef.current = null;
    };
  }, [map, censusYear, geoLevel]);

  // Effect 2: update data and colours without reloading tiles.
  useEffect(() => {
    updateValuesRef.current?.();
  }, [
    charId,
    charName,
    value,
    colourCount,
    equalWidth,
  ]);

  return null;
}

const clickHandlerRef = { current: null };
