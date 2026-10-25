export function buildTileStyle({ apiUrl, tileUrl, tileSourceLayer, promoteId }) {
  return {
    version: 8,
    sources: {
      census: {
        type: 'vector',
        url: `pmtiles://${apiUrl}${tileUrl}`,
        promoteId: promoteId,
        minzoom: 0,
      },
    },
    layers: [
      { id: 'census-fill', type: 'fill', source: 'census',
        'source-layer': tileSourceLayer,
        paint: { 'fill-color': '#3388ff', 'fill-opacity': 0.95 } },
      { id: 'census-outline', type: 'line', source: 'census',
        'source-layer': tileSourceLayer,
        paint: { 'line-color': '#333', 'line-width': 1 } },
    ],
  };
}