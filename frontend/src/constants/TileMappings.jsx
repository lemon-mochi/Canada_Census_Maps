import { 
    geoCodeIDs81,
    geoCodeIDs86,
    geoCodeIDs91,
    geoCodeIDs96,
    geoCodeIDs_01_16
} from "@/constants/GeoCodeIDs.jsx";

// -----------------------------------------------------------------------------------------------------
// IMPORTANT: There are certain cases where the geoCode in the vector tile is a number and not a string.
// the following unordered set keeps track of such cases.
// -----------------------------------------------------------------------------------------------------
export const NUMBER_VALUE_GEO_LEVELS = new Map([
  [
    2021,
    new Set([
      'Federal electoral district (2023 Representation Order)',
    ]),
  ],
  [
    1991,
    new Set([
      'Province',
      'Census division',
      'Census subdivision',
    ]),
  ],
  [
    1986,
    new Set([
      'Province',
      'Census subdivision',
    ]),
  ],
  [
    1981,
    new Set([
      'Province',
      'Census division',
      'Census subdivision',
    ]),
  ],
  [
    1976,
    new Set([
        'Province',
    ]),
  ],
  [
    1971,
    new Set([
        'Province',
    ])
  ],
  [
    1961,
    new Set([
        'Province',
    ])
  ],
  [
    1951,
    new Set([
        'Province',
    ])
  ],  
]);

export function getPromoteID(censusYear, geoLevel) {
  if (censusYear === 2021) {
    if (geoLevel === 'Federal electoral district (2023 Representation Order)') {
        return 'FED_NUM';
    }

    return 'DGUID';
  }

  if (censusYear >= 2001) {
    return geoCodeIDs_01_16[geoLevel];
  }

  if (censusYear === 1996) {
    return geoCodeIDs96[geoLevel];
  }

  if (censusYear === 1991) {
    return geoCodeIDs91[geoLevel];
  }

  if (censusYear === 1986) {
    return geoCodeIDs86[geoLevel];
  }

  // 1951, 1961, 1971, 1976 use 1981's vector tiles.
  if (censusYear >= 1951 && censusYear <= 1981) {
    return geoCodeIDs81[geoLevel];
  }

  return null;
}

export function getTileID(censusYear, geoLevel, geoCode) {
    if (censusYear === 2021) {
        if (geoLevel === 'Federal electoral district (2023 Representation Order)') {
            // example: geoCode is 2023A000459002
            // only need 59002 for FED_NUM
            return geoCode.substring(9, 14);
        }
        return geoCode;
    }

    if (censusYear >= 2010) {
        return geoCode;
    }

    if (
        censusYear === 2006 ||
        censusYear === 2001 ||
        censusYear === 1996 ||
        censusYear === 1991
    ) {
        if (
            geoLevel === 'Census tract' || geoLevel === 'Dissemination area'
        ) {
            return geoToTile.get(geoCode);
        }

        return geoCode;
    }

    // if here, the census year is 1986 or 1981
    return geoCode;
    
}
