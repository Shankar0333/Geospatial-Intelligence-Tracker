import { useMemo } from 'react'

import { AircraftState, DefenseEvent, LayerKey } from '../types'

interface Props {
  aircraft: AircraftState[]
  defense: DefenseEvent[]
  layers: Record<LayerKey, boolean>
}

export function MapViewport({ aircraft, defense, layers }: Props) {
  const summary = useMemo(() => {
    const parts = []
    if (layers.air) parts.push(`Aircraft: ${aircraft.length}`)
    if (layers.defense) parts.push(`Defense events: ${defense.length}`)
    return parts.join(' • ')
  }, [aircraft.length, defense.length, layers.air, layers.defense])

  return (
    <section style={{ border: '1px solid #233', borderRadius: 8, padding: 16, minHeight: 300 }}>
      <h3>3D World Map (Cesium / Mapbox integration point)</h3>
      <p>{summary || 'No active layers selected.'}</p>
      <p>
        This panel is wired for map engines. Hook CesiumJS Viewer or Mapbox GL here and render entity layers,
        airspace polygons, geofences, and heatmaps.
      </p>
    </section>
  )
}
