import { getColValue } from '@/constants/Columns.jsx';

export function buildPopupHtml({ promoteId, apiYear, charName, value, actualValue }) {
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
            GeoCode: ${promoteId ?? 'N/A'}
            </h4>
            <div><strong>Census year:</strong> ${apiYear}</div>
            <div><strong>Characteristic:</strong> ${charName ?? 'N/A'}</div>
            <div><strong>Column:</strong> ${
            getColValue(apiYear, value) ?? 'nothing here'
            }</div>
            <div><strong>Value:</strong> ${actualValue ?? 'N/A'}</div>
        </div>
    `;

    return popupHtml;
}