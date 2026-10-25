
import { useEffect, useRef } from 'react';
import { useMap } from 'react-leaflet';
import { API_URL } from '@/constants/ApiURL.jsx';
import { toApiYear } from '@/constants/CensusYears.jsx';
import {
  getPromoteID,
  getTileID,
  NUMBER_VALUE_GEO_LEVELS
} from '@/constants/TileMappings.jsx';
import {
  getGeoCode
} from '@/constants/GeoMappings.jsx';
import L from 'leaflet';
import { maplibreGL } from '@maplibre/maplibre-gl-leaflet';
import 'maplibre-gl/dist/maplibre-gl.css';
import { buildTileStyle } from '@/constants/buildTileStyle.js';
import { buildPopupHtml } from '@/constants/buildPopupHtml.js';
import { fetchColourExpression } from '@/constants/fetchColourExpression.js';

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
  const clickHandlerRef = useRef(null);

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

        const style = buildTileStyle({
          apiUrl: API_URL,
          tileUrl: tileInfo.url,
          tileSourceLayer: tileInfo.source_layer,
          promoteId: getPromoteID(apiYear, geoLevel),
        });

        layer = maplibreGL({
          pane: 'vectorPane',
          interactive: true,
          style: style,
        });

        maplibreLayerRef.current = layer;
        layer.addTo(map);

        mapLibreMap = layer.getMaplibreMap();
        mapLibreMapRef.current = mapLibreMap;

        const canvas = mapLibreMap.getCanvas();
        if (canvas) {
          canvas.style.pointerEvents = 'auto';
        }

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
                .map(feature => getGeoCode(apiYear, geoLevel, feature))
                .filter(id => id != null)
                .map(String),
            ),
          ];

          if (geoCodes.length === 0) {
            settings.setBoundaries?.([]);
            return;
          }

          const result = await fetchColourExpression({
            apiYear,
            geoLevel,
            geoCodes,
            settings,
            valueCache,
          });

          if (!result || !isMounted) return;

          settings.setBoundaries?.(result.boundaries);

          if (
            result.expression &&
            mapLibreMap.getLayer('census-fill')
          ) {
            mapLibreMap.setPaintProperty(
              'census-fill',
              'fill-color',
              result.expression,
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

          const popupHtml = buildPopupHtml({
            promoteId: properties[promoteId],
            apiYear: apiYear,
            charName: settings.charName,
            value: settings.value,
            actualValue: actualValue
          });

          popupRef.current?.remove();

          popupRef.current = L.popup()
            .setLatLng(e.latlng)
            .setContent(popupHtml)
            .openOn(map);
        }

        map.on('click', handleFeatureClick);

        mapLibreMap.on('load', () => {
          if (isMounted) {
            updateVisibleValues();
          }
        });

        mapLibreMap.on('moveend', updateVisibleValues);

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