import React, { useState, useEffect } from 'react';

const CensusForm = () => {
  const [censusYear, setCensusYear] = useState('2021');
  const [geoLevel, setGeoLevel] = useState('auto');
  const [chars, setChars] = useState([]); 

  const censusYears = [
    '1871', '1881', '1891', '1901', '1911', '1921', '1931', '1941', '1951',
    '1961', '1971', '1981', '1991', '1996', '2001', '2006', '2011',
    '2016', '2021'
  ];
  
  const geoLevels_2021 = [
    { value: 'auto', label: 'Automatically decide based on zoom level' },
    { value: 'Province', label: 'Provinces/Territories' },
    { value: 'Census division', label: 'Census divisions' },
    { value: 'Census subdivision', label: 'Census subdivisions' },
    { value: 'Federal electoral district (2023 Representation Order)', label: 'Federal electoral districts (2023 Representation Order)' },
    { value: 'Federal electoral district (2013 Representation Order)', label: 'Federal electoral districts (2013 Representation Order)' },
    { value: 'Aggregate dissemination area', label: 'Aggregate dissemination areas' },
    { value: 'Dissemination area', label: 'Dissemination areas' },
  ];

  // Fetch characteristics when censusYear changes or component mounts
  useEffect(() => {
    async function get_characteristics() {
      try {
        // Pass censusYear to backend if your endpoint accepts query params
        const res = await fetch(`http://localhost:8000/api/characteristics`);
        const json = await res.json();
        console.log("json.data", json);
        setChars(Array.isArray(json) ? json : json.data || []);
      } catch (err) {
        console.error("Failed to load census characteristics:", err);
      }
    }

    get_characteristics();
  }, [censusYear]);

  return (
    <div>
      {/* Census Year Dropdown */}
      <label htmlFor="census_year">Choose census year:</label>
      <select
        id="census_year"
        name="census_year"
        value={censusYear}
        onChange={(e) => setCensusYear(e.target.value)}
      >
        {censusYears.map((year) => (
          <option key={year} value={year}>
            {year}
          </option>
        ))}
      </select>

      <br />

      {/* Geographic Level Dropdown */}
      <label htmlFor="geo_level">Choose geographic level:</label>
      <select
        id="geo_level"
        name="geo_level"
        value={geoLevel}
        onChange={(e) => setGeoLevel(e.target.value)}
      >
        {geoLevels_2021.map((option, index) => (
          <option key={`${option.value}-${index}`} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      {/* Characteristics List */}
      <div style={{ marginTop: '1rem' }}>
        {chars && chars.map((char) => (
          <button 
            key={char.CHARACTERISTIC_ID} 
            id={char.CHARACTERISTIC_ID}
          >
            {char.CHARACTERISTIC_NAME}
          </button>
        ))}
      </div>
    </div>
  );
};

export default CensusForm;