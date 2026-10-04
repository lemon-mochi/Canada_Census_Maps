import { useState } from 'react';
import CensusMap from './components/Map.jsx';
import CensusForm from './components/CensusForm.jsx';
import './styles/globals.scss';

function App() {
  const [censusYear, setCensusYear] = useState('2021');
  const [geoLevel, setGeoLevel] = useState('Province');
  const [charId, setCharId] = useState(1);
  const [value, setValue] = useState(1); 

  return (
    <div className="container">
      <CensusMap
        censusYear={censusYear}
        geoLevel={geoLevel}
        charId={charId}
        value={value}
      />

      <CensusForm
        censusYear={censusYear}
        setCensusYear={setCensusYear}
        geoLevel={geoLevel}
        setGeoLevel={setGeoLevel}
      />
    </div>
  );
}

export default App;