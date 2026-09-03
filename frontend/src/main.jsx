import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Map from './components/Map.jsx'
import CensusForm from './components/CensusForm.jsx'
import "./styles/globals.scss"

createRoot(document.getElementById('root')).render(
  <div className="container">
    <Map></Map>
    <CensusForm></CensusForm>
  </div>
  
)
