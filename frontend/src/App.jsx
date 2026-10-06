import { useState } from 'react';
import CensusMap from './components/Map.jsx';
import CensusForm from './components/CensusForm.jsx';
import './styles/globals.scss';

function App() {
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

  return (
    <div className="container">
      <CensusMap
        censusYear={censusYear}
        geoLevel={geoLevel}
        charId={charId}
        value={value}
        colourCount={colourCount}
        equalWidth={equalWidth}
      />

      <CensusForm
        censusYear={censusYear}
        setCensusYear={setCensusYear}
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