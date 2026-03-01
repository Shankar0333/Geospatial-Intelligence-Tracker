import { Alert } from '../types'

export function AlertsPanel({ alerts }: { alerts: Alert[] }) {
  return (
    <section>
      <h3>Alerts</h3>
      <ul>
        {alerts.map((alert) => (
          <li key={alert.id}>
            <strong>[{alert.severity.toUpperCase()}]</strong> {alert.title} — {alert.detail}
          </li>
        ))}
      </ul>
    </section>
  )
}
