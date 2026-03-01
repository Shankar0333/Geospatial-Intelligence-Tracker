import { AircraftState, DefenseEvent, HeatmapBin, LayerKey } from '../types'

interface Props {
  aircraft: AircraftState[]
  defense: DefenseEvent[]
  heatmap: HeatmapBin[]
  layers: Record<LayerKey, boolean>
}

export function MapViewport({ aircraft, defense, heatmap, layers }: Props) {
  const topCells = heatmap.slice(0, 5)

  return (
    <section style={{ border: '1px solid #233', borderRadius: 8, padding: 16, minHeight: 300 }}>
      <h3>3D World Map Command View</h3>
      <p>
        Integration-ready shell for CesiumJS / Mapbox GL / Google Maps. Use this layer model to render live tracks,
        geofences, airspace polygons, and defense events.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
        <div>
          <h4>Live Layer Snapshot</h4>
          <ul>
            {layers.air && <li>Air entities: {aircraft.length}</li>}
            {layers.defense && <li>Defense events: {defense.length}</li>}
            {layers.land && <li>Land layer enabled</li>}
            {layers.sea && <li>Sea layer enabled</li>}
          </ul>
        </div>
        <div>
          <h4>Air-Traffic Hotspots</h4>
          <ol>
            {topCells.map((cell) => (
              <li key={`${cell.latitude}-${cell.longitude}`}>
                {cell.latitude}, {cell.longitude} — {cell.count} aircraft
              </li>
            ))}
          </ol>
        </div>
      </div>
    </section>
  )
}
