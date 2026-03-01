import { CameraFeed } from '../types'

export function CameraGrid({ cameras }: { cameras: CameraFeed[] }) {
  return (
    <section>
      <h3>Public Traffic Cameras</h3>
      <ul>
        {cameras.map((camera) => (
          <li key={camera.id}>
            <a href={camera.stream_url} target="_blank" rel="noreferrer">
              {camera.name}
            </a>{' '}
            ({camera.region})
          </li>
        ))}
      </ul>
    </section>
  )
}
