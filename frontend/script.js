// Path to PMTiles file hosted by FastAPI
const protocol = new pmtiles.Protocol();
maplibregl.addProtocol("pmtiles", protocol.tile);

const PMTILES_URL =
    "http://localhost:8000/tiles_output/lpr_000b21a_e.pmtiles";

const testPMTiles = new pmtiles.PMTiles(PMTILES_URL); 

const SOURCE_LAYER = "lpr_000b21a_e";

const p = new pmtiles.PMTiles(PMTILES_URL);
protocol.add(p);

const map = new maplibregl.Map({
    container: 'map',
    style: {
        version: 8,
        sources: {
            'osm-basemap': {
                type: 'raster',
                tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
                tileSize: 256
            },
            'provincial-vector-source': {
                type: 'vector',
                url: `pmtiles://${PMTILES_URL}`,
                promoteId: 'PRUID' // Assigns PRUID property directly to feature.id
            }
        },
        layers: [
            {
                id: 'basemap',
                type: 'raster',
                source: 'osm-basemap'
            },
            {
                id: 'province-fill',
                type: 'fill',
                source: 'provincial-vector-source',
                'source-layer': SOURCE_LAYER,
                paint: {
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['feature-state', 'pop_2021'],
                        0,       '#f7fbff',
                        100000,  '#c6dbef',
                        1000000, '#6baed6',
                        4000000, '#2171b5',
                        8000000, '#08306b'
                    ],
                    'fill-opacity': 0.75
                }
            },
            {
                id: 'province-borders',
                type: 'line',
                source: 'provincial-vector-source',
                'source-layer': SOURCE_LAYER,
                paint: {
                    'line-color': '#ffffff',
                    'line-width': 1.2
                }
            }
        ]
    },
    center: [-98.5795, 56.1304],
    zoom: 3.5
});

let populationData = {};

// 2. Fetch population lookup dict
async function loadPopulationData() {
    try {
        const res = await fetch('http://localhost:8000/api/province-population');
        const json = await res.json();

        console.log(json);
        
        // Normalize object keys to strings for safe matching
        populationData = {};
        for (const [key, val] of Object.entries(json)) {
            populationData[String(key)] = val;
        }

        updateMapFeatureStates();
    } catch (err) {
        console.error("Failed to load census population:", err);
    }
}

// 3. Map population values onto vector features
function updateMapFeatureStates() {
    if (!Object.keys(populationData).length) return;

    // Retrieve loaded features in current view
    const features = map.querySourceFeatures('provincial-vector-source', {
        sourceLayer: SOURCE_LAYER
    });

    features.forEach(feature => {
        // feature.id exists because promoteId: 'PRUID' was set
        if (feature.id !== undefined && feature.id !== null) {
            const key = String(feature.id);
            const pop = populationData[key];

            if (pop !== undefined) {
                map.setFeatureState(
                    {
                        source: 'provincial-vector-source',
                        sourceLayer: SOURCE_LAYER,
                        id: feature.id
                    },
                    { pop_2021: pop }
                );
            }
        }
    });
}

// Trigger state updates when map loads or new tiles render
map.on('load', loadPopulationData);

map.on('sourcedata', (e) => {
    if (e.isSourceLoaded && e.sourceId === 'provincial-vector-source') {
        updateMapFeatureStates();
    }
});

// 4. On-click Popup
map.on('click', 'province-fill', (e) => {
    if (!e.features.length) return;

    const feature = e.features[0];
    const props = feature.properties;
    const pruid = String(feature.id || props.PRUID);
    const provName = props.PRENAME || props.PRNAME || "Province";
    const pop = populationData[pruid] ? populationData[pruid].toLocaleString() : "N/A";

    new maplibregl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`<strong>${provName}</strong><br/>2021 Population: ${pop}`)
        .addTo(map);
});

map.on('mouseenter', 'province-fill', () => map.getCanvas().style.cursor = 'pointer');
map.on('mouseleave', 'province-fill', () => map.getCanvas().style.cursor = '');