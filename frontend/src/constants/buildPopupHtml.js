import { getColValue } from '@/constants/Columns.jsx';


function getCensusProfile(apiYear, geoCode) {
    if (apiYear === 2021) {
        return `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/page.cfm?Lang=E&DGUIDlist=${geoCode}&GENDERlist=1,2,3&STATISTIClist=1,4&HEADERlist=0`;
    }
}

export function buildPopupHtml({ geoCode, apiYear, charName, value, actualValue }) {
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
            <a 
                href=${getCensusProfile(apiYear, geoCode)}
                target="_blank">
                    Source
            </a>
        </div>
    `;

    return popupHtml;
}