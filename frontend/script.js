// Path to PMTiles file hosted by FastAPI
const protocol = new pmtiles.Protocol();
maplibregl.addProtocol("pmtiles", protocol.tile);

var PMTILES_URL =
    "http://localhost:8000/tiles_output/lpr_000b21a_e.pmtiles";

const testPMTiles = new pmtiles.PMTiles(PMTILES_URL); 

var SOURCE_LAYER = "lpr_000b21a_e";

var p = new pmtiles.PMTiles(PMTILES_URL);
protocol.add(p);

var censusYear = "2021"


const map = new maplibregl.Map({
    container: 'map',
    style: {
        version: 8,
        sources: {
            'osm-basemap': {
                type: 'raster',
                tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
                tileSize: 256,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            },
            'geo-vector-source': {
                type: 'vector',
                url: `pmtiles://${PMTILES_URL}`,
                promoteId: 'PRUID', // Assigns PRUID property directly to feature.id
            }
        },
        layers: [
            {
                id: 'basemap',
                type: 'raster',
                source: 'osm-basemap'
            },
            {
                id: 'area-fill',
                type: 'fill',
                source: 'geo-vector-source',
                'source-layer': SOURCE_LAYER,
                paint: {
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['feature-state', 'pop'],
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
                id: 'area-borders',
                type: 'line',
                source: 'geo-vector-source',
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

function getPromoteId(geoLevel) {
    const idFields = {
        lpr: 'PRUID',
        lcd: 'CDUID',
        lcsd: 'CSDUID',
        lfed: 'FEDUID',
        lct: 'CTUID',
        lda: 'DAUID'
    };

    return idFields[geoLevel];
}

function updateMapSource(geoLevel, censusYear) {
    const lastTwo = String(censusYear).slice(-2);

    console.log(lastTwo);

    if (String(geoLevel).length == 3) {
        SOURCE_LAYER = `${geoLevel}_000b${lastTwo}a_e`;
    } else {
        SOURCE_LAYER = `${geoLevel}000b${lastTwo}a_e`;
    }
        
    PMTILES_URL =
        `http://localhost:8000/tiles_output/${SOURCE_LAYER}.pmtiles`;

    // Remove the old layers and source
    if (map.getLayer('area-fill')) {
        map.removeLayer('area-fill');
    }

    if (map.getLayer('area-borders')) {
        map.removeLayer('area-borders');
    }

    if (map.getSource('geo-vector-source')) {
        map.removeSource('geo-vector-source');
    }

    // Add the new PMTiles source
    p = new pmtiles.PMTiles(PMTILES_URL);
    protocol.add(p);

    map.addSource('geo-vector-source', {
        type: 'vector',
        url: `pmtiles://${PMTILES_URL}`,
        promoteId: getPromoteId(geoLevel)
    });

    // Add the layers back using the new source-layer
    map.addLayer({
        id: 'area-fill',
        type: 'fill',
        source: 'geo-vector-source',
        'source-layer': SOURCE_LAYER,
        paint: {
            'fill-color': [
                'interpolate',
                ['linear'],
                ['feature-state', 'pop'],
                0,       '#f7fbff',
                100000,  '#c6dbef',
                1000000, '#6baed6',
                4000000, '#2171b5',
                8000000, '#08306b'
            ],
            'fill-opacity': 0.75
        }
    });

    map.addLayer({
        id: 'area-borders',
        type: 'line',
        source: 'geo-vector-source',
        'source-layer': SOURCE_LAYER,
        paint: {
            'line-color': '#ffffff',
            'line-width': 1.2
        }
    });
}


let populationData = {};

// Fetch population lookup dict
async function loadPopulationData(census_year="2021", geoLevel="lpr") {
    console.log("in loadPopulationData. census_year is: ", census_year);
    try {
        const res = await fetch(
            `http://localhost:8000/api/population?geo_level=${geoLevel}`
        );
        const json = await res.json();

        console.log(json);
        
        // Normalize object keys to strings for safe matching
        populationData = {};
        for (const [key, val] of Object.entries(json)) {
            populationData[String(key)] = val;
        }

        updateMapSource(geoLevel, census_year);

        updateMapFeatureStates();
    } catch (err) {
        console.error("Failed to load census population:", err);
    }
}

// Map population values onto vector features
function updateMapFeatureStates() {
    if (!Object.keys(populationData).length) return;

    // Retrieve loaded features in current view
    const features = map.querySourceFeatures('geo-vector-source', {
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
                        source: 'geo-vector-source',
                        sourceLayer: SOURCE_LAYER,
                        id: feature.id
                    },
                    { pop: pop }
                );
            }
        }
    });
}

// Trigger state updates when map loads or new tiles render
map.on('load', loadPopulationData(censusYear="2021", geoLevel="lpr"));

map.on('sourcedata', (e) => {
    if (e.isSourceLoaded && e.sourceId === 'geo-vector-source') {
        updateMapFeatureStates();
    }
});

// 4. On-click Popup
map.on('click', 'area-fill', (e) => {
    if (!e.features.length) return;

    const feature = e.features[0];
    const props = feature.properties;
    const pruid = String(feature.id || props.PRUID);
    const provName = props.PRENAME || props.PRNAME || "Area";
    const pop = populationData[pruid] ? populationData[pruid].toLocaleString() : "N/A";

    new maplibregl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`<strong>${provName}</strong><br/>${censusYear} Population: ${pop}`)
        .addTo(map);
});

map.on('mouseenter', 'area-fill', () => map.getCanvas().style.cursor = 'pointer');
map.on('mouseleave', 'area-fill', () => map.getCanvas().style.cursor = '');