import { FormEvent, useEffect, useMemo, useState } from 'react'

import { AlertsPanel } from './components/AlertsPanel'
import { CameraGrid } from './components/CameraGrid'
import { DomainActivity } from './components/DomainActivity'
import { LayerToggles } from './components/LayerToggles'
import { MapViewport } from './components/MapViewport'
import { api, setToken } from './hooks/useApi'
import {
  Alert,
  AircraftState,
  CameraFeed,
  DefenseEvent,
  HeatmapBin,
  LandEvent,
  LayerKey,
  RiskAssessment,
  SeaVessel,
  TrafficDensitySnapshot
} from './types'

const WS_URL = (import.meta.env.VITE_WS_URL as string | undefined) ?? 'ws://localhost:8000/api/ws/air'

function App() {
  const [username, setUsername] = useState('analyst')
  const [password, setPassword] = useState('analyst123')
  const [token, setJwtToken] = useState<string | null>(null)
  const [isAuthed, setIsAuthed] = useState(false)
  const [authError, setAuthError] = useState<string | null>(null)

  const [aircraft, setAircraft] = useState<AircraftState[]>([])
  const [cameras, setCameras] = useState<CameraFeed[]>([])
  const [defense, setDefense] = useState<DefenseEvent[]>([])
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [heatmap, setHeatmap] = useState<HeatmapBin[]>([])
  const [density, setDensity] = useState<TrafficDensitySnapshot | null>(null)
  const [risk, setRisk] = useState<RiskAssessment | null>(null)
  const [sea, setSea] = useState<SeaVessel[]>([])
  const [land, setLand] = useState<LandEvent[]>([])

  const [layers, setLayers] = useState<Record<LayerKey, boolean>>({ air: true, land: true, sea: true, defense: true })

  const authenticate = async (event?: FormEvent) => {
    event?.preventDefault()
    setAuthError(null)
    try {
      const tokenRes = await api.post('/auth/token', { username, password })
      setToken(tokenRes.data.access_token)
      setJwtToken(tokenRes.data.access_token)
      setIsAuthed(true)
    } catch {
      setAuthError('Login failed. Check credentials.')
    }
  }

  useEffect(() => {
    if (!isAuthed) return

    const load = async () => {
      const [airRes, cameraRes, defenseRes, alertRes, heatmapRes, densityRes, riskRes, seaRes, landRes] = await Promise.all([
        api.get('/aircraft'),
        api.get('/cameras'),
        api.get('/defense'),
        api.get('/alerts'),
        api.get('/heatmap'),
        api.get('/analytics/traffic-density'),
        api.get('/analytics/risk'),
        api.get('/sea'),
        api.get('/land')
      ])
      setAircraft(airRes.data)
      setCameras(cameraRes.data)
      setDefense(defenseRes.data)
      setAlerts(alertRes.data)
      setHeatmap(heatmapRes.data)
      setDensity(densityRes.data)
      setRisk(riskRes.data)
      setSea(seaRes.data)
      setLand(landRes.data)
    }

    load().catch(console.error)
    const timer = window.setInterval(() => load().catch(console.error), 12000)

    if (!token) return () => window.clearInterval(timer)

    const ws = new WebSocket(`${WS_URL}?token=${encodeURIComponent(token)}`)
    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data) as AircraftState[]
      setAircraft(payload)
    }

    return () => {
      window.clearInterval(timer)
      ws.close()
    }
  }, [isAuthed, token])

  const toggleLayer = (key: LayerKey) => setLayers((prev) => ({ ...prev, [key]: !prev[key] }))

  const airborneAvgSpeed = useMemo(() => {
    const values = aircraft.map((a) => a.velocity_ms).filter((v): v is number => typeof v === 'number')
    if (!values.length) return 0
    return Math.round(values.reduce((sum, v) => sum + v, 0) / values.length)
  }, [aircraft])

  if (!isAuthed) {
    return (
      <main style={{ margin: '100px auto', maxWidth: 460, padding: 20, color: '#d8e1e8', backgroundColor: '#101820' }}>
        <h1>Geospatial Intelligence Tracker</h1>
        <form onSubmit={authenticate}>
          <label style={{ display: 'block' }}>Username<input value={username} onChange={(e) => setUsername(e.target.value)} style={{ width: '100%' }} /></label>
          <label style={{ display: 'block', marginTop: 10 }}>Password<input value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: '100%' }} type="password" /></label>
          <button type="submit" style={{ marginTop: 12 }}>Sign In</button>
          {authError && <p style={{ color: '#ff7b7b' }}>{authError}</p>}
        </form>
      </main>
    )
  }

  return (
    <main style={{ margin: '0 auto', maxWidth: 1280, padding: 20, color: '#d8e1e8', backgroundColor: '#101820' }}>
      <h1>Geospatial Intelligence Tracker</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 12, marginBottom: 16 }}>
        <div style={{ border: '1px solid #2d3f52', borderRadius: 8, padding: 10 }}>Aircraft: {aircraft.length}</div>
        <div style={{ border: '1px solid #2d3f52', borderRadius: 8, padding: 10 }}>Avg speed: {airborneAvgSpeed} m/s</div>
        <div style={{ border: '1px solid #2d3f52', borderRadius: 8, padding: 10 }}>Open alerts: {alerts.length}</div>
        <div style={{ border: '1px solid #2d3f52', borderRadius: 8, padding: 10 }}>Density: {density?.total_aircraft ?? 0}</div>
        <div style={{ border: '1px solid #2d3f52', borderRadius: 8, padding: 10 }}>Risk: {risk?.level ?? 'n/a'} ({risk?.overall_score ?? 0})</div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '250px 1fr', gap: 16 }}>
        <LayerToggles layers={layers} onToggle={toggleLayer} />
        <MapViewport aircraft={aircraft} defense={defense} heatmap={heatmap} layers={layers} />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16, marginTop: 16 }}>
        <AlertsPanel alerts={alerts} />
        <CameraGrid cameras={cameras} />
        <DomainActivity sea={sea} land={land} />
      </div>
    </main>
  )
}

export default App
