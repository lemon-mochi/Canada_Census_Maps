import { useState, useEffect } from 'react';
import CensusMap from './components/Map.jsx';
import CensusForm from './components/CensusForm.jsx';
import './styles/globals.scss';
import { geoLevelsFor } from './constants/Constants.jsx';
import { loadGeoMappings } from './constants/TileMappings.jsx'

function App() {
  useEffect(() => {
    loadGeoMappings();
  })
  const [censusYear, setCensusYear] = useState('2021');
  const [geoLevel, setGeoLevel] = useState('Province');

  const [charId, setCharId] = useState(1);
  const [charName, setCharName] = useState("Population, 2021");
  const [value, setValue] = useState(1);

  const [colourCount, setColourCount] = useState(5);
  const [equalWidth, setEqualWidth] = useState(true);

  const handleSelect = ({
    charId,
    columnId,
    charName
  }) => {
    setCharId(charId);
    setValue(columnId);
    setCharName(charName);
  };

  const handleCensusYearChange = (year) => {
    setCensusYear(year);

    const levels = geoLevelsFor(year);
    const firstLevel = levels.find(
      (level) => level.value !== 'auto'
    );

    if (firstLevel) {
      setGeoLevel(firstLevel.value);
    }

    setCharId(null);
    setCharName(null);
    setValue(null);
  };

  return (
    <div className="container">
      <CensusMap
        censusYear={censusYear}
        geoLevel={geoLevel}
        charId={charId}
        charName={charName}
        value={value}
        colourCount={colourCount}
        equalWidth={equalWidth}
        handleFeatureClick={handleCensusYearChange}
      />

      <CensusForm
        censusYear={censusYear}
        setCensusYear={handleCensusYearChange}
        geoLevel={geoLevel}
        setGeoLevel={setGeoLevel}
        onSelect={handleSelect}
        onColourCountChange={setColourCount}
        onEqualWidthChange={setEqualWidth}
        charName={charName}
        columnId={value}
      />
    </div>
  );
}

export default App;