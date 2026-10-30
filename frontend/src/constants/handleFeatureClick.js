import L from 'leaflet';
import { getPromoteID } from '@/constants/TileMappings.jsx';
import { buildPopupHtml } from '@/constants/buildPopupHtml.js';

export function handleFeatureClick(e, settingsRef, dependencies) {
    const {
        mapLibreMap,
        apiYear,
        geoLevel,
        valueCache,
        popupRef,
        map,
    } = dependencies;

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
        apiYear,
        charName: settings.charName,
        value: settings.value,
        actualValue,
    });

    popupRef.current?.remove();

    popupRef.current = L.popup()
        .setLatLng(e.latlng)
        .setContent(popupHtml)
        .openOn(map);
}