import { Alert } from '../types'

const severityColor: Record<string, string> = {
  high: '#ff7b7b',
  medium: '#f8c555',
  low: '#79d2ff'
}

export function AlertsPanel({ alerts }: { alerts: Alert[] }) {
  return (
    <section>
      <h3>Alert Stream</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {alerts.map((alert) => (
          <li key={alert.id} style={{ marginBottom: 8 }}>
            <strong style={{ color: severityColor[alert.severity] ?? '#ddd' }}>[{alert.severity.toUpperCase()}]</strong>{' '}
            {alert.title} — {alert.detail}
          </li>
        ))}
      </ul>
    </section>
  )
}
