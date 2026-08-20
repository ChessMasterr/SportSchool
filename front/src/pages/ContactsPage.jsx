import { useEffect, useState } from 'react'
import { api, paginateResults } from '../api'

const FACILITY_TYPE_LABELS = {
  pool: 'Бассейн',
  gym: 'Тренажёрный зал',
  game_hall: 'Игровой зал',
  combat_hall: 'Зал единоборств',
  tennis: 'Теннисные корты',
  other: 'Спортивный объект',
}

export default function ContactsPage() {
  const [facilities, setFacilities] = useState([])
  const [settings, setSettings] = useState(null)
  const [competitions, setCompetitions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.getFacilities(),
      api.getSiteSettings(),
      api.getCompetitions(),
    ])
      .then(([fac, set, comp]) => {
        setFacilities(paginateResults(fac))
        setSettings(set)
        setCompetitions(paginateResults(comp))
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>Контакты</h1>
          <p>Адреса, телефоны и режим работы спортивных объектов</p>
        </div>
      </div>

      <section className="section">
        <div className="container">
          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : (
            <>
              <div className="contact-grid">
                {facilities.map((fac) => (
                  <div key={fac.id} className="contact-card">
                    <h3>{fac.name}</h3>
                    <p>
                      <span className="tag">
                        {FACILITY_TYPE_LABELS[fac.facility_type] || fac.facility_type}
                      </span>
                    </p>
                    <p>📍 {fac.address}</p>
                    {fac.phone && (
                      <p>📞 <a href={`tel:${fac.phone.replace(/\D/g, '')}`}>{fac.phone}</a></p>
                    )}
                    {fac.phone_admin && (
                      <p>Администрация: <a href={`tel:${fac.phone_admin.replace(/\D/g, '')}`}>{fac.phone_admin}</a></p>
                    )}
                    {fac.working_hours && (
                      <p>🕐 {fac.working_hours}</p>
                    )}
                    {fac.description && <p>{fac.description}</p>}
                    {fac.has_hall_rental && (
                      <div className="notice" style={{ marginTop: 12 }}>
                        {fac.hall_rental_note || 'Возможна аренда зала. Звоните по указанному телефону.'}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {settings && (settings.email || settings.vk_url) && (
                <div style={{ marginTop: 48 }}>
                  <h2 className="section__title">Общие контакты</h2>
                  <div className="contact-card" style={{ maxWidth: 400 }}>
                    {settings.email && (
                      <p>✉️ <a href={`mailto:${settings.email}`}>{settings.email}</a></p>
                    )}
                    {settings.vk_url && (
                      <p><a href={settings.vk_url} target="_blank" rel="noreferrer">ВКонтакте</a></p>
                    )}
                    {settings.telegram_url && (
                      <p><a href={settings.telegram_url} target="_blank" rel="noreferrer">Telegram</a></p>
                    )}
                  </div>
                </div>
              )}

              {competitions.length > 0 && (
                <div style={{ marginTop: 48 }}>
                  <h2 className="section__title">Календарь соревнований</h2>
                  <div className="table-wrap">
                    <table>
                      <thead>
                        <tr>
                          <th>Дата</th>
                          <th>Название</th>
                          <th>Место</th>
                        </tr>
                      </thead>
                      <tbody>
                        {competitions.map((c) => (
                          <tr key={c.id}>
                            <td>{c.event_date}</td>
                            <td>{c.title}</td>
                            <td>{c.location || '—'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </section>
    </>
  )
}
