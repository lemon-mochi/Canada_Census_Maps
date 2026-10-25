import {
  getTileID,
  NUMBER_VALUE_GEO_LEVELS
} from '@/constants/TileMappings.jsx';
import { API_URL } from '@/constants/ApiURL.jsx';

// Fetch and apply values to the currently visible features.
export async function fetchColourExpression({
  apiYear,
  geoLevel,
  geoCodes,
  settings,
  valueCache 
}) {

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

  if (!response.ok) {
    return null;
  }

  const result = await response.json();
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

  if (expression.length === 1) 
    return { boundaries: result.boundaries ?? [], expression: null };

  expression.push('#cccccc');

  return { boundaries: result.boundaries ?? [], expression };
}