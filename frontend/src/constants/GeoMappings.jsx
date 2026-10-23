import { API_URL } from "@/constants/ApiURL.jsx";
import { 
    geoCodeIDs81,
    geoCodeIDs86,
    geoCodeIDs91,
    geoCodeIDs96,
    geoCodeIDs_01_16
} from "@/constants/GeoCodeIDs.jsx";

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
let ct_01_mappings;
let da_01_mappings;
let ct_06_mappings;
let da_06_mappings;

export async function loadGeoMappings() {
    ct_96_mappings = await get_geo_mappings(1996, "Census tract");
    ct_01_mappings = await get_geo_mappings(2001, "Census tract");
    da_01_mappings = await get_geo_mappings(2001, "Dissemination area");
    ct_06_mappings = await get_geo_mappings(2006, "Census tract");
    da_06_mappings = await get_geo_mappings(2006, "Dissemination area");
}

// this will track how geo codes map to tile ids.
const geoToTile = new Map();

export function getGeoCode(censusYear, geoLevel, feature) {
    const properties = feature.properties;
    var ret;
    var tileID;

    if (censusYear === 2021) {
        if (geoLevel === 'Federal electoral district (2023 Representation Order)') {
            ret = '2023A0004' + properties.FED_NUM;
            return ret;
        }
        return properties.DGUID;
    }

    if (censusYear >= 2010) {
        return properties[geoCodeIDs_01_16[geoLevel]];
    }

    if (censusYear === 2006) {
        tileID = properties[geoCodeIDs_01_16[geoLevel]];
        if (geoLevel === 'Census tract') {

            ret = ct_06_mappings[tileID];
            geoToTile.set(
                ret,
                tileID
            );
            return ret;
        }

        if (geoLevel === 'Dissemination area') {

            ret = da_06_mappings[tileID];
            geoToTile.set(
                ret,
                tileID
            );
            return ret;
        }

        return tileID;
    }

    if (censusYear === 2001) {
        tileID = properties[geoCodeIDs_01_16[geoLevel]];
        if (geoLevel === 'Census tract') {

            ret = ct_01_mappings[tileID];
            geoToTile.set(
                ret,
                tileID
            );
            return ret;
        }

        if (geoLevel === 'Dissemination area') {

            ret = da_01_mappings[tileID];
            geoToTile.set(
                ret,
                tileID
            );            
            return ret;
        }

        return tileID;
    }

    if (censusYear === 1996) {
        tileID = properties[geoCodeIDs96[geoLevel]];
        if (geoLevel === 'Census tract') {

            ret = ct_96_mappings[tileID];
            geoToTile.set(
                ret,
                tileID
            );
            return ret;
        }

        return tileID;
    }

    if (censusYear === 1991) {
        if (geoLevel === 'Census tract') {

            ret = cleanCT1991(
                properties.CA,
                properties.PROV,
                properties.CT_CODE
            );
            geoToTile.set(
                ret,
                properties[geoCodeIDs91[geoLevel]]
            );

            return ret;
        }

        return properties[geoCodeIDs91[geoLevel]];
    }

    if (censusYear === 1986) {
        return properties[geoCodeIDs86[geoLevel]];
    }

    if (censusYear >= 1951 && censusYear <= 1981) {
        return properties[geoCodeIDs81[geoLevel]];
    }
}