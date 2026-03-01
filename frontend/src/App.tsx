import { useEffect, useState } from 'react'

import { AlertsPanel } from './components/AlertsPanel'
import { CameraGrid } from './components/CameraGrid'
import { LayerToggles } from './components/LayerToggles'
import { MapViewport } from './components/MapViewport'
import { api, setToken } from './hooks/useApi'
import { Alert, AircraftState, CameraFeed, DefenseEvent, LayerKey } from './types'

function App() {
  const [aircraft, setAircraft] = useState<AircraftState[]>([])
  const [cameras, setCameras] = useState<CameraFeed[]>([])
  const [defense, setDefense] = useState<DefenseEvent[]>([])
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [layers, setLayers] = useState<Record<LayerKey, boolean>>({
    air: true,
    land: false,
    sea: false,
    defense: true
  })

  useEffect(() => {
    const bootstrap = async () => {
      const tokenRes = await api.post('/auth/token', { username: 'analyst', password: 'analyst123' })
      setToken(tokenRes.data.access_token)

      const [airRes, cameraRes, defenseRes, alertRes] = await Promise.all([
        api.get('/aircraft'),
        api.get('/cameras'),
        api.get('/defense'),
        api.get('/alerts')
      ])

      setAircraft(airRes.data)
      setCameras(cameraRes.data)
      setDefense(defenseRes.data)
      setAlerts(alertRes.data)
    }

    bootstrap().catch(console.error)
  }, [])

  const toggleLayer = (key: LayerKey) => {
    setLayers((prev) => ({ ...prev, [key]: !prev[key] }))
  }

  return (
    <main style={{ margin: '0 auto', maxWidth: 1200, padding: 20, color: '#d8e1e8', backgroundColor: '#101820' }}>
      <h1>Geospatial Intelligence Tracker</h1>
      <p>
        Live ADS-B aircraft tracking, geofencing, anomaly alerts, defense OSINT overlays, and public traffic camera
        monitoring.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '250px 1fr', gap: 16 }}>
        <LayerToggles layers={layers} onToggle={toggleLayer} />
        <MapViewport aircraft={aircraft} defense={defense} layers={layers} />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginTop: 16 }}>
        <AlertsPanel alerts={alerts} />
        <CameraGrid cameras={cameras} />
      </div>
    </main>
  )
}

export default App
