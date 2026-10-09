import { useEffect, useRef } from 'react';
import { useMap } from 'react-leaflet';
import {
  API_URL,
  toApiYear,
  getColValue
} from '@/constants/Constants.jsx';
import {
  getPromoteID,
  getGeoCode,
  getTileID
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
}) {
  const map = useMap();

  const maplibreLayerRef = useRef(null);
  const valueCache = useRef(new Map());
  const popupRef = useRef(null);

  useEffect(() => {
    if (!censusYear || !geoLevel || geoLevel === 'auto') {
      return;
    }

    let isMounted = true;
    let mapLibreMap = null;

    const apiYear = toApiYear(censusYear);

    async function updateVisibleValues() {
      if (!mapLibreMap) return;

      if (charId == null || value == null) {
        return;
      }

      let features = mapLibreMap.queryRenderedFeatures({
        layers: ['census-fill'],
      });

      const geoCodes = [
        ...new Set(
          features
            .map(feature =>
              getGeoCode(
                apiYear,
                geoLevel,
                feature,
              )
            )
            .filter(
              id => id !== undefined && id !== null,
            )
            .map(String),
        ),
      ];

      if (geoCodes.length === 0) return;

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
            char_id: charId,
            value,
            num_colours: colourCount,
            equal_width: equalWidth,
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

      const expression = ['case'];

      for (const item of data) {
        if (!Array.isArray(item.colour)) {
          continue;
        }

        const tileID = getTileID(apiYear, geoLevel, item.geo_code);

        // if (tileID == null) {
        //   continue;
        // }

        const colour = item.colour;

        valueCache.current.set(String(tileID), item.value);

        expression.push(
          ['==', ['id'], String(tileID)],
          `rgb(${colour[0]}, ${colour[1]}, ${colour[2]})`,
        );
      }

      if (expression.length === 1) {
        return;
      }

      expression.push('#cccccc');

      mapLibreMap.setPaintProperty(
        'census-fill',
        'fill-color',
        expression,
      );
    }

    function handleFeatureClick(e) {
      if (!mapLibreMap) return;

      const point = mapLibreMap.project([
        e.latlng.lng,
        e.latlng.lat,
      ]);

      const features = mapLibreMap.queryRenderedFeatures(point, {
        layers: ['census-fill'],
      });

      if (!features.length) return;

      const properties = features[0].properties;


      const promoteId = getPromoteID(
        apiYear,
        geoLevel
      );

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

          <div>
            <strong>Census year:</strong> ${apiYear}
          </div>

          <div>
            <strong>Characteristic:</strong> ${charName ?? 'N/A'}
          </div>

          <div>
            <strong>Column:</strong> ${
              getColValue(apiYear, value)
              ?? 'nothing here'
            }
          </div>

          <div>
            <strong>Value:</strong> ${
              actualValue ?? 'N/A'
            }
          </div>
        </div>
      `;

      if (popupRef.current) {
        popupRef.current.remove();
      }

      popupRef.current = L.popup()
        .setLatLng(e.latlng)
        .setContent(popupHtml)
        .openOn(map);
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
          interactive: true,

          style: {
            version: 8,

            sources: {
              census: {
                type: 'vector',
                url: `pmtiles://${API_URL}${data.url}`,
                promoteId: getPromoteID(apiYear, geoLevel),
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
                  'fill-opacity': 0.95,
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

        const canvas = mapLibreMap.getCanvas();
        if (canvas) {
          canvas.style.pointerEvents = 'auto';
        }

        map.on('click', handleFeatureClick);

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

      if (popupRef.current) {
        popupRef.current.remove();
        popupRef.current = null;
      }

      if (mapLibreMap) {
        mapLibreMap.off('moveend', updateVisibleValues);
      }

      if (
        maplibreLayerRef.current &&
        map.hasLayer(maplibreLayerRef.current)
      ) {
        map.removeLayer(
          maplibreLayerRef.current,
        );
        map.off('click', handleFeatureClick);

        maplibreLayerRef.current = null;
      }
    };
  }, [
    map,
    censusYear,
    geoLevel,
    charId,
    charName,
    value,
    colourCount,
    equalWidth,
  ]);

  return null;
}