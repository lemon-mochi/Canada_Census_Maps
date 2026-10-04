import { useState } from 'react';
import Map from './components/Map.jsx';
import CensusForm from './components/CensusForm.jsx';
import './styles/globals.scss';

function App() {
  const [censusYear, setCensusYear] = useState('2021');
  const [geoLevel, setGeoLevel] = useState('Province');

  return (
    <div className="container">
      <Map
        censusYear={censusYear}
        geoLevel={geoLevel}
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