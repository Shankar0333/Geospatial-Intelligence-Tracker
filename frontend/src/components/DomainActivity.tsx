import { LandEvent, SeaVessel } from '../types'

interface Props {
  sea: SeaVessel[]
  land: LandEvent[]
}

export function DomainActivity({ sea, land }: Props) {
  return (
    <section>
      <h3>Land / Sea Activity</h3>
      <p>Sea tracks: {sea.length} • Land events: {land.length}</p>
      <ul>
        {sea.slice(0, 2).map((v) => (
          <li key={v.id}>SEA: {v.name} ({v.vessel_type}) @ {v.speed_knots} kn</li>
        ))}
        {land.slice(0, 2).map((e) => (
          <li key={e.id}>LAND: {e.title} ({e.category})</li>
        ))}
      </ul>
    </section>
  )
}
