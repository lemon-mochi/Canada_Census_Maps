import { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import {
  GeoSearchControl,
  OpenStreetMapProvider,
} from 'leaflet-geosearch';

import 'leaflet-geosearch/dist/geosearch.css';

export default function LocationSearch() {
  const map = useMap();

  useEffect(() => {
    const provider = new OpenStreetMapProvider();

    const searchControl = new GeoSearchControl({
      provider,
      style: 'bar',
      position: 'topleft',
      searchLabel: 'Search locations...',
      autoClose: true,
      keepResult: true,
      showMarker: false,
      animateZoom: true,
    });

    map.addControl(searchControl);

    return () => {
      map.removeControl(searchControl);
    };
  }, [map]);

  return null;
}