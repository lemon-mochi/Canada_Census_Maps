const NHS_DA_LABEL = '2011 NHS DA';
// The backend uses 2010 to mean "2011 NHS dissemination areas".
const NHS_DA_API_YEAR = 2010;

export const CENSUS_YEARS = [
  '1871 (Coming soon)',
  '1881 (Coming soon)',
  '1891 (Coming soon)',
  '1901 (Coming soon)',
  '1911 (Coming soon)',
  '1921 (Coming soon)',
  '1931 (Coming soon)',
  '1941 (Coming soon)',
  '1951 (Coming soon)',
  '1961 (Coming soon)',
  '1971 (Coming soon)',
  '1976 (Coming soon)',
  '1981',
  '1986',
  '1991',
  '1996',
  '2001',
  '2006',
  '2011',
  NHS_DA_LABEL,
  '2016',
  '2021',
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
  1976: 'https://publications.gc.ca/site/eng/9.836486/publication.html',
  1971: 'https://publications.gc.ca/site/eng/9.834259/publication.html',
  1961: 'https://publications.gc.ca/site/eng/9.831044/publication.html',
  1951: 'https://publications.gc.ca/site/eng/9.836019/publication.html',
  1941: 'https://publications.gc.ca/site/eng/9.833108/publication.html',
  1931: 'https://publications.gc.ca/site/eng/9.832354/publication.html',
  1921: 'https://publications.gc.ca/site/eng/9.830574/publication.html',
  1911: 'https://publications.gc.ca/site/eng/9.828391/publication.html',
  1901: 'https://publications.gc.ca/site/eng/9.828258/publication.html',
  1891: 'https://publications.gc.ca/site/eng/9.828079/publication.html',
  1881: 'https://publications.gc.ca/site/eng/9.828009/publication.html',
  1871: 'https://publications.gc.ca/site/eng/9.827965/publication.html'
};

const GEO_LEVELS_2021 = [
  { value: 'auto', label: 'Automatically decide based on zoom level (Coming soon)' },
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
  { value: 'auto', label: 'Automatically decide based on zoom level (Coming soon)' },
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
  { value: 'auto', label: 'Automatically decide based on zoom level (Coming soon)' },
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
  { value: 'auto', label: 'Automatically decide based on zoom level (Coming soon)' },
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
  { value: 'auto', label: 'Automatically decide based on zoom level (Coming soon)' },
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
  { value: 'auto', label: 'Automatically decide based on zoom level (Coming soon)' },
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
  { value: 'auto', label: 'Automatically decide based on zoom level (Coming soon)' },
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
  { value: 'auto', label: 'Automatically decide based on zoom level (Coming soon)' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  { value: 'Census tract', label: 'Census tracts' },
]

const GEO_LEVELS_1981 = [
  { value: 'auto', label: 'Automatically decide based on zoom level (Coming soon)' },
  { value: 'Canada', label: 'Canada' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  { value: 'Census tract', label: 'Census tracts' },
]

const GEO_LEVELS_OLD = [
  { value: 'auto', label: 'Automatically decide based on zoom level (Coming soon)' },
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

export const toApiYear = (censusYear) =>
  censusYear === NHS_DA_LABEL ? NHS_DA_API_YEAR : parseInt(censusYear, 10);