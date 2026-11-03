import { getColValue } from '@/constants/Columns.jsx';


function getCensusProfile(apiYear, geoCode, geoLevel, charId) {
    if (apiYear === 2021) {
        return `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/page.cfm?Lang=E&DGUIDlist=${geoCode}&GENDERlist=1,2,3&STATISTIClist=1,4&HEADERlist=0`;
    } else if (apiYear === 2016) {
        // for 2016 the geographic level matters
        if (geoLevel === "Canada" || geoLevel === "Province") {
            // 2 is for Canada and Provinces/Territories
            // Statcan treats Canada as a province for some reason. That is why there 
            return `https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/page.cfm?Lang=E&Geo1=PR&Code1=${geoCode}&B1=All&TABID=3&type=0`;  
        } else if (geoLevel === "Census division") {
            // census divisions
            return `https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/page.cfm?Lang=E&Geo1=CD&Code1=${geoCode}&B1=All&TABID=3&type=0`;
        } else if (geoLevel === "Census subdivision") {
            // census subdivisions
            return `https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/page.cfm?Lang=E&Geo1=CSD&Code1=${geoCode}&B1=All&TABID=3&type=0`;
        } else if (geoLevel === "Federal electoral district (2013 Representation Order)") {
            // federal electoral districts
            return `https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/page.cfm?Lang=E&Geo1=FED&Code1=${geoCode}&B1=All&TABID=3&type=0`;
        } else if (geoLevel === "Aggregate dissemination area") {
            // aggregate dissemination areas
            return `https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/page.cfm?Lang=E&Geo1=ADA&Code1=${geoCode}&B1=All&TABID=3&type=0`;
        } else {
            // dissemination area
            return `https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/page.cfm?Lang=E&Geo1=DA&Code1=${geoCode}&B1=All&TABID=3&type=0`;
        }   
    } else if (apiYear === 2011) {
        // for 2011, there is the census profile and the NHS profile. 
        // Characteristic ID 1 to 472 is census. Anything higher is NHS.
        if (charId <= 472) {
            if (geoLevel === "Canada" || geoLevel === "Province") {
                return `https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=PR&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&B1=All&Custom=&TABID=3`;
            } else if (geoLevel === "Census division") {
                return `https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=CD&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&B1=All&Custom=&TABID=3`;
            } else if (geoLevel === "Census subdivision") {
                return `https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=CSD&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&B1=All&Custom=&TABID=3`;
            } else if (geoLevel === "Federal electoral district (2003 Representation Order)") {
                return `https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=FED&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&B1=All&Custom=&TABID=3`;
            } else if (geoLevel === "Census tract") {
                // TODO: this does not work. There is a different code.
                return null;
            } else {
                // dissemination area
                return `https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=DA&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&B1=All&Custom=&TABID=3`;
            }
        } else {
            // NHS profile
            if (geoLevel === "Canada" || geoLevel === "Province") {
                return `https://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=PR&Code1=${geoCode}&Data=Count&SearchText=01&SearchType=Begins&SearchPR=01&A1=All&B1=All&Custom=&TABID=3`;
            } else if (geoLevel === "Census division") {
                return `https://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=CD&Code1=${geoCode}&Data=Count&SearchText=01&SearchType=Begins&SearchPR=01&A1=All&B1=All&Custom=&TABID=3`;
            } else if (geoLevel === "Census subdivision") {
                return `https://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=CSD&Code1=${geoCode}&Data=Count&SearchText=01&SearchType=Begins&SearchPR=01&A1=All&B1=All&Custom=&TABID=3`;
            } else if (geoLevel === "Federal electoral district (2003 Representation Order)") {
                return `https://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/page.cfm?Lang=E&Geo1=FED&Code1=${geoCode}&Data=Count&SearchText=01&SearchType=Begins&SearchPR=01&A1=All&B1=All&Custom=&TABID=3`;
            } else if (geoLevel === "Census tract") {
                // TODO: this does not work. There is a different code.
                return null;
            } // 2011 NHS DAs are a special case. Census year is set to 2010 for that case.
        }
    } else if (apiYear === 2010) {
        // special case for 2011 NHS DAs
        return "https://borealisdata.ca/file.xhtml?fileId=7750&version=6.3";
    } else if (apiYear === 2006) {
        if (geoLevel === "Canada" || geoLevel === "Province") {
            return `https://www12.statcan.gc.ca/census-recensement/2006/dp-pd/prof/92-591/details/page.cfm?Lang=E&Geo1=PR&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&SearchText=Canada&SearchType=Begins&SearchPR=01&B1=All&Custom=`;
        } else if (geoLevel === "Census division") {
            return `https://www12.statcan.gc.ca/census-recensement/2006/dp-pd/prof/92-591/details/page.cfm?Lang=E&Geo1=CD&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&SearchText=Canada&SearchType=Begins&SearchPR=01&B1=All&Custom=`;
        } else if (geoLevel === "Census subdivision") {
            return `https://www12.statcan.gc.ca/census-recensement/2006/dp-pd/prof/92-591/details/page.cfm?Lang=E&Geo1=CSD&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&SearchText=Canada&SearchType=Begins&SearchPR=01&B1=All&Custom=`;
        } else if (geoLevel === "Federal electoral district (2003 Representation Order)") {
            return null;
        } else if (geoLevel === "Census tract") {
            return null;
        } else {
            // dissemination area
            return null;
        }
    } else if (apiYear === 2001) {
        if (geoLevel === "Canada" || geoLevel === "Province") {
            return `https://www12.statcan.gc.ca/english/profil01/CP01/Details/Page.cfm?Lang=E&Geo1=PR&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&SearchText=Canada&SearchType=Begins&SearchPR=01&B1=All&Custom=`;
        } else if (geoLevel === "Census division") {
            return `https://www12.statcan.gc.ca/english/profil01/CP01/Details/Page.cfm?Lang=E&Geo1=CD&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&SearchText=Canada&SearchType=Begins&SearchPR=01&B1=All&Custom=`;
        } else if (geoLevel === "Census subdivision") {
            return `https://www12.statcan.gc.ca/english/profil01/CP01/Details/Page.cfm?Lang=E&Geo1=CSD&Code1=${geoCode}&Geo2=PR&Code2=01&Data=Count&SearchText=Canada&SearchType=Begins&SearchPR=01&B1=All&Custom=`;
        } else if (geoLevel === "Federal electoral district (1996 Representation Order)") {
            return null;
        } else if (geoLevel === "Census tract") {
            return null;
        } else {
            // dissemination area
            return null;
        }
    } else if (apiYear === 1996) {
        
    }
}

export function buildPopupHtml({ 
    geoCode,
    apiYear,
    charName,
    value,
    actualValue,
    geoLevel,
    charId
}) {
    const link = getCensusProfile(apiYear, geoCode, geoLevel, charId);
    const popupHtml = `
        <div style="
            max-height: 200px;
            overflow-y: auto;
            font-family: sans-serif;
            font-size: 13px;
        ">
            <h4 style="
            margin: 0 0 8px 0;
            font-size: 14px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 4px;
            ">
            GeoCode: ${geoCode ?? 'N/A'}
            </h4>
            <div><strong>Census year:</strong> ${apiYear}</div>
            <div><strong>Characteristic:</strong> ${charName ?? 'N/A'}</div>
            <div><strong>Column:</strong> ${
            getColValue(apiYear, value) ?? 'nothing here'
            }</div>
            <div><strong>Value:</strong> ${actualValue ?? 'N/A'}</div>
            ${link
                ? `<a href="${link}" target="_blank">Source</a>`
                : 'No link'
            }
        </div>
    `;

    return popupHtml;
}