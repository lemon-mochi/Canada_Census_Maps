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
