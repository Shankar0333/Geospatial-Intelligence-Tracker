import { LayerKey } from '../types'

interface Props {
  layers: Record<LayerKey, boolean>
  onToggle: (key: LayerKey) => void
}

export function LayerToggles({ layers, onToggle }: Props) {
  return (
    <div>
      <h3>Layers</h3>
      {(Object.keys(layers) as LayerKey[]).map((key) => (
        <label key={key} style={{ display: 'block', textTransform: 'capitalize' }}>
          <input type="checkbox" checked={layers[key]} onChange={() => onToggle(key)} /> {key}
        </label>
      ))}
    </div>
  )
}
