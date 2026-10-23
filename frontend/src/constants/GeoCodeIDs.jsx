// this works for 2016, 2011, and most of 2006 and 2001 (except for Census tracts and dissemination areas)
export const geoCodeIDs_01_16 = {
    'Canada': 'GEO_CODE',
    'Province': 'PRUID',
    'Census division': 'CDUID',
    'Census subdivision': 'CSDUID',
    'Federal electoral district (2013 Representation Order)': 'FEDUID',
    'Aggregate dissemination area': 'ADAUID',
    'Dissemination area': 'DAUID',
    'Federal electoral district (2003 Representation Order)': 'FEDUID',
    'Census tract': 'CTUID',
    'Federal electoral district (1996 Representation Order)': 'FEDUID',
};

// this works for 1996
export const geoCodeIDs96 = {
    'Canada': 'GEO_CODE',
    'Province': 'PRuid',
    'Census division': 'CDuid',
    'Census subdivision': 'CSDuid',
    'Federal electoral district (1996 Representation Order)': 'FEDuid',
    'Census tract': 'CTuid',
    'Enumeration area': 'EAuid'
};

// for 1991 census tracts. The database (parquet) stores GEO_CODE as SCA970593983
// that is the same as SCA + CA + PROV + CT_CODE in the vector tile
// CA = 970, PROV = 59, CT_CODE = 3983 
function cleanCT1991(CA, PROV, CT_CODE) {
  return 'SCA' + CA + PROV + CT_CODE;
};

export const geoCodeIDs91 = {
    'Canada': 'GEO_CODE',
    'Province': 'PROV',
    'Census division': 'CD',
    'Census subdivision': 'CSD',
    'Federal electoral district (1987 Representation Order)': 'FED',
    'Census tract': 'CA_CTNAME'
  // census tracts is a special case (look at the function above)
};

export const geoCodeIDs86 = {
    'Canada': 'GEO_CODE',
    'Province': 'PR_ID',
    'Census division': 'CD86',
    'Census subdivision': 'CSD86_ID',
    'Census tract': 'geosid'
};

export const geoCodeIDs81 = {
    'Canada': 'GEO_CODE',
    'Province': 'PROV81',
    'Census division': 'CD81',
    'Census subdivision': 'CSD81',
    'Census tract': 'geosid'
};
