export type LayerKey = 'air' | 'land' | 'sea' | 'defense'

export interface AircraftState {
  icao24: string
  callsign?: string
  latitude: number
  longitude: number
  altitude_m?: number
  velocity_ms?: number
  heading_deg?: number
}

export interface Alert {
  id: string
  severity: string
  title: string
  detail: string
  entity_id: string
  created_at: string
}

export interface CameraFeed {
  id: string
  name: string
  region: string
  stream_url: string
  source: string
  status: string
}

export interface DefenseEvent {
  id: string
  category: string
  title: string
  description: string
  latitude: number
  longitude: number
  source_url: string
  occurred_at: string
}
