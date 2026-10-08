import { API_URL } from "@/constants/Constants.jsx";

async function get_geo_mappings(apiYear, geoLevel) {
    try {
        const response = await fetch(
            `${API_URL}/api/geo_mappings?census_year=${apiYear}&geo_level=${geoLevel}`,    
        );
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const mappings = await response.json();
        return mappings;
    } catch (err) {
        console.error('Failed to load geographic mappings', err);
    }
};

let ct_96_mappings;
let da_96_mappings;
let ct_01_mappings;
let da_01_mappings;
let ct_06_mappings;
let da_06_mappings;

export async function loadGeoMappings() {
    ct_96_mappings = await get_geo_mappings(1996, "Census tract");
    da_96_mappings = await get_geo_mappings(1996, "Dissemination area");
    ct_01_mappings = await get_geo_mappings(2001, "Census tract");
    da_01_mappings = await get_geo_mappings(2001, "Dissemination area");
    ct_06_mappings = await get_geo_mappings(2006, "Census tract");
    da_06_mappings = await get_geo_mappings(2006, "Dissemination area");
}

// this works for 2016, 2011, and most of 2006 and 2001 (except for Census tracts and dissemination areas)
const geoCodeIDs_01_16 = {
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
const geoCodeIDs96 = {
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

const geoCodeIDs91 = {
  'Province': 'PROV',
  'Census division': 'CD',
  'Census subdivision': 'CSD',
  'Federal electoral district (1987 Representation Order)': 'FED'
  // census tracts is a special case (look at the function above)
};

const geoCodeIDs86 = {
  'Province': 'PR_ID',
  'Census division': 'CD86',
  'Census subdivision': 'CSD86_ID',
  'Census tract': 'geosid'
};

const geoCodeIDs81 = {
  'Province': 'PROV81',
  'Census division': 'CD81',
  'Census subdivision': 'CSD81',
  'Census tract': 'geosid'
};

export function getTileID(censusYear, geoLevel) {
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

  if (censusYear === 1981) {
    return geoCodeIDs81[geoLevel];
  }

  return null;
}


export function getGeoCode(censusYear, geoLevel, feature) {
    const properties = feature.properties;

    if (censusYear === 2021) {
        if (geoLevel === 'Federal electoral district (2023 Representation Order)') {
            return '2023A0004' + properties.FED_NUM;
        }

        return properties.DGUID;
    }

    if (censusYear >= 2010) {
        return properties[geoCodeIDs_01_16[geoLevel]];
    }

    if (censusYear === 2006) {
        if (geoLevel === 'Census tract') {
            return ct_06_mappings[properties[geoCodeIDs_01_16[geoLevel]]];
        }

        if (geoLevel === 'Dissemination area') {
            return da_06_mappings[properties[geoCodeIDs_01_16[geoLevel]]];
        }

        return properties[geoCodeIDs_01_16[geoLevel]];
    }

    if (censusYear === 2001) {
        if (geoLevel === 'Census tract') {
            return ct_01_mappings[properties[geoCodeIDs_01_16[geoLevel]]];
        }

        if (geoLevel === 'Dissemination area') {
            return da_01_mappings[properties[geoCodeIDs_01_16[geoLevel]]];
        }

        return properties[geoCodeIDs_01_16[geoLevel]];
    }

    if (censusYear === 1996) {
        if (geoLevel === 'Census tract') {
            console.log("ct 96 mapping: ", ct_96_mappings[properties[geoCodeIDs96[geoLevel]]]);
            return ct_96_mappings[properties[geoCodeIDs96[geoLevel]]];
        }

        if (geoLevel === 'Dissemination area') {
            return da_96_mappings[properties[geoLevel]];
        }

        return properties[geoCodeIDs96[geoLevel]];
    }

    if (censusYear === 1991) {
        if (geoLevel === 'Census tract') {
            return cleanCT1991(
                properties.CA,
                properties.PROV,
                properties.CT_CODE
            );
        }

        return properties[geoCodeIDs91[geoLevel]];
    }

    if (censusYear === 1986) {
        return properties[geoCodeIDs86[geoLevel]];
    }

    if (censusYear === 1981) {
        return properties[geoCodeIDs81[geoLevel]];
    }
}