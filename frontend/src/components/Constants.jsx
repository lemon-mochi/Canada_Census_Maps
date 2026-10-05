/* ------------------------------------------------------------------ */
/* Constants (outside the component so they aren't recreated per render) */
/* ------------------------------------------------------------------ */

// Vite: VITE_API_URL in .env. Next.js: NEXT_PUBLIC_API_URL. Falls back to local dev.
export const API_URL =
  import.meta.env?.VITE_API_URL ??
  (typeof process !== 'undefined' ? import.meta.env?.NEXT_PUBLIC_API_URL : undefined) ??
  'http://localhost:8000';

const NHS_DA_LABEL = '2011 NHS DA';
// The backend uses 2010 to mean "2011 NHS dissemination areas".
const NHS_DA_API_YEAR = 2010;

export const CENSUS_YEARS = [
  '1871', '1881', '1891', '1901', '1911', '1921', '1931', '1941', '1951',
  '1961', '1971', '1981', '1986', '1991', '1996', '2001', '2006', '2011',
  NHS_DA_LABEL, '2016', '2021',
];

export const SOURCES = {
  2021: 'https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/index.cfm?Lang=E',
  2016: 'https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/index.cfm?Lang=E',
  2011: 'https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/index-eng.cfm',
  [NHS_DA_LABEL]: 'https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/index-eng.cfm',
  2006: 'https://www12.statcan.gc.ca/census-recensement/2006/index-eng.cfm',
  2001: 'https://www12.statcan.gc.ca/english/census01/home/Index.cfm',
  1996: 'https://www12.statcan.gc.ca/english/census01/info/census96.cfm',
  1991: 'https://www12.statcan.gc.ca/datasets/Index-eng.cfm?Temporal=1991',
  1986: 'https://www12.statcan.gc.ca/datasets/Index-eng.cfm?Temporal=1986',
  1981: 'https://www12.statcan.gc.ca/datasets/Index-eng.cfm?Temporal=1981',
};

const GEO_LEVELS_2021 = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  {
    value: 'Federal electoral district (2023 Representation Order)',
    label: 'Federal electoral districts (2023 Representation Order)',
  },
  {
    value: 'Federal electoral district (2013 Representation Order)',
    label: 'Federal electoral districts (2013 Representation Order)',
  },
  { value: 'Aggregate dissemination area', label: 'Aggregate dissemination areas' },
  { value: 'Dissemination area', label: 'Dissemination areas' },
];

const GEO_LEVELS_2016 = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  {
    value: 'Federal electoral district (2013 Representation Order)',
    label: 'Federal electoral districts (2013 Representation Order)',
  },
  { value: 'Aggregate dissemination area', label: 'Aggregate dissemination areas' },
  { value: 'Dissemination area', label: 'Dissemination areas' },
];

const GEO_LEVELS_2011 = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  {
    value: 'Federal electoral district (2003 Representation Order)',
    label: 'Federal electoral districts (2003 Representation Order)',
  },
  { value: 'Census tract', label: 'Census tracts' },
  { value: 'Dissemination area', label: 'Dissemination areas' },
];

// use 2010 for 2011 NHS DAs
const GEO_LEVELS_2010 = [
  { value: 'Dissemination area', label: 'Dissemination areas' },
]

const GEO_LEVELS_2006 = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  {
    value: 'Federal electoral district (2003 Representation Order)',
    label: 'Federal electoral districts (2003 Representation Order)',
  },
  { value: 'Census tract', label: 'Census tracts' },
  { value: 'Dissemination area', label: 'Dissemination areas' },
];

const GEO_LEVELS_2001 = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  {
    value: 'Federal electoral district (1996 Representation Order)',
    label: 'Federal electoral districts (1996 Representation Order)',
  },
  { value: 'Census tract', label: 'Census tracts' },
  { value: 'Dissemination area', label: 'Dissemination areas' },
];

const GEO_LEVELS_1996 = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  {
    value: 'Federal electoral district (1996 Representation Order)',
    label: 'Federal electoral districts (1996 Representation Order)',
  },
  { value: 'Census tract', label: 'Census tracts' },
  { value: 'Enumeration area', label: 'Enumeration areas' },
]

const GEO_LEVELS_1991 = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  {
    value: 'Federal electoral district (1987 Representation Order)',
    label: 'Federal electoral districts (1987 Representation Order)',
  },
  { value: 'Census tract', label: 'Census tracts' },
]

const GEO_LEVELS_1986 = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  { value: 'Census tract', label: 'Census tracts' },
]

const GEO_LEVELS_1981 = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  { value: 'Census tract', label: 'Census tracts' },
]

const GEO_LEVELS_OLD = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
]

const GEO_LEVELS_BY_YEAR = {
  2021: GEO_LEVELS_2021,
  2016: GEO_LEVELS_2016,
  2011: GEO_LEVELS_2011,
  2010: GEO_LEVELS_2010,
  2006: GEO_LEVELS_2006,
  2001: GEO_LEVELS_2001,
  1996: GEO_LEVELS_1996,
  1991: GEO_LEVELS_1991,
  1986: GEO_LEVELS_1986,
  1981: GEO_LEVELS_1981,
};

export const geoLevelsFor = (censusYear) => {
  // 2011 NHS DAs are represented by 2010 in the backend.
  if (censusYear === NHS_DA_LABEL) {
    return GEO_LEVELS_2010;
  }

  return GEO_LEVELS_BY_YEAR[censusYear] ?? GEO_LEVELS_OLD;
};

export const COLUMN_LABELS = {
  C1_COUNT_TOTAL: 'C1_T',
  'C2_COUNT_MEN+': 'C2_M',
  'C3_COUNT_WOMEN+': 'C3_F',
  C10_RATE_TOTAL: 'C4_R',
  'C11_RATE_MEN+': 'C5_R',
  'C12_RATE_WOMEN+': 'C6_R',
  COUNT_TOTAL: 'C_T',
  COUNT_MALE: 'C_M',
  COUNT_FEMALE: 'C_F',
  RATE_TOTAL: 'R_T',
  RATE_MALE: 'R_M',
  RATE_FEMALE: 'R_F',
};

export const toApiYear = (censusYear) =>
  censusYear === NHS_DA_LABEL ? NHS_DA_API_YEAR : parseInt(censusYear, 10);

/* ------------------------------------------------------------------ */
/* Data helpers                                                         */
/* ------------------------------------------------------------------ */

/*
 * Turn the flat, ordered list from the backend into a tree using each
 * item's `level` (0 = top level):
 *
 * Population
 *   └── Age groups
 *       └── 0 to 14
 *           └── 0 to 4
 */
export const buildTree = (characteristics) => {
  const root = [];
  const stack = [];

  characteristics.forEach((char) => {
    const node = { ...char, children: [] };

    // Pop back up to this node's parent.
    while (stack.length > 0 && stack[stack.length - 1].level >= node.level) {
      stack.pop();
    }

    if (stack.length === 0) {
      root.push(node);
    } else {
      stack[stack.length - 1].children.push(node);
    }

    stack.push(node);
  });

  return root;
};

export const LIGHTEST_BLUE = [247, 251, 255];
export const DARKEST_BLUE = [8, 48, 107];

export function getColourPalette(numColours) {
  if (numColours <= 1) {
    return [DARKEST_BLUE];
  }

  return Array.from({ length: numColours }, (_, index) => {
    return LIGHTEST_BLUE.map((start, i) => {
      const end = DARKEST_BLUE[i];

      return Math.round(
        start +
          ((end - start) * index) /
            (numColours - 1)
      );
    });
  });
}