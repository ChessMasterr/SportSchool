import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, formatTime, paginateResults } from '../api'

export default function DirectionDetailPage() {
  const { slug } = useParams()
  const [direction, setDirection] = useState(null)
  const [schedule, setSchedule] = useState([])
  const [coaches, setCoaches] = useState([])
  const [priceDoc, setPriceDoc] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    setLoading(true)
    setError(false)

    api.getSportDirection(slug)
      .then(async (dir) => {
        setDirection(dir)
        const [sch, coachList, docs] = await Promise.all([
          api.getSchedule({ sport_direction: dir.id }),
          api.getCoaches({ sport_direction: dir.id }),
          dir.school_slug ? api.getDocuments({ school_slug: dir.school_slug, doc_type: 'price_list' }) : Promise.resolve([]),
        ])
        setSchedule(paginateResults(sch))
        setCoaches(paginateResults(coachList))
        const list = paginateResults(docs)
        setPriceDoc(list[0] || null)
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false))
  }, [slug])

  if (loading) return <div className="loading">Загрузка...</div>

  if (error || !direction) {
    return (
      <section className="section">
        <div className="container">
          <div className="empty">Секция не найдена</div>
          <div style={{ textAlign: 'center', marginTop: 24 }}>
            <Link to="/directions" className="btn btn--blue">Все секции</Link>
          </div>
        </div>
      </section>
    )
  }

  return (
    <>
      <div className="page-header">
        <div className="container">
          <p className="breadcrumb">
            <Link to="/">Главная</Link>
            {' / '}
            <Link to="/directions">Секции</Link>
            {' / '}
            <span>{direction.name}</span>
          </p>
          <h1>{direction.name}</h1>
          {direction.school_name && <p>{direction.school_name}</p>}
        </div>
      </div>

      <section className="section">
        <div className="container detail-layout">
          <div className="detail-main">
            {direction.photo_url && (
              <img
                src={direction.photo_url}
                alt={direction.name}
                className="detail-photo"
              />
            )}

            {direction.description && (
              <div className="card" style={{ marginBottom: 24 }}>
                <div className="card__body">
                  <h2 className="card__title">О секции</h2>
                  <p className="card__text">{direction.description}</p>
                  {direction.age_from && (
                    <p className="card__text" style={{ marginTop: 12 }}>
                      <strong>Возраст:</strong> {direction.age_from}
                      {direction.age_to ? `–${direction.age_to}` : '+'} лет
                    </p>
                  )}
                  {direction.level_display && (
                    <span className="tag" style={{ marginTop: 8 }}>
                      {direction.level_display}
                    </span>
                  )}
                  {direction.requirements && (
                    <div className="notice" style={{ marginTop: 16 }}>
                      <strong>Требования:</strong> {direction.requirements}
                    </div>
                  )}
                </div>
              </div>
            )}

            <div className="card" style={{ marginBottom: 24 }}>
              <div className="card__body">
                <h2 className="card__title">Расписание</h2>
                {schedule.length === 0 ? (
                  <div className="empty" style={{ padding: '24px 0' }}>
                    Расписание для этой секции пока не опубликовано.
                    Актуальную информацию уточняйте по телефону объекта.
                  </div>
                ) : (
                  <div className="table-wrap">
                    <table>
                      <thead>
                        <tr>
                          <th>День</th>
                          <th>Время</th>
                          <th>Группа</th>
                          <th>Тренер</th>
                          <th>Объект</th>
                        </tr>
                      </thead>
                      <tbody>
                        {schedule.map((row) => (
                          <tr key={row.id}>
                            <td>{row.weekday_display}</td>
                            <td>
                              {formatTime(row.time_start)}–{formatTime(row.time_end)}
                            </td>
                            <td>{row.age_group || row.group_name || '—'}</td>
                            <td>{row.coach_name || '—'}</td>
                            <td>{row.facility_name || '—'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
                <div style={{ marginTop: 16 }}>
                  <Link
                    to={`/schedule?sport=${direction.id}`}
                    className="btn btn--blue"
                  >
                    Полное расписание
                  </Link>
                </div>

                {direction.school_slug && (
                  <div style={{ marginTop: 12 }}>
                    {priceDoc?.file_url ? (
                      <a
                        href={priceDoc.file_url}
                        target="_blank"
                        rel="noreferrer"
                        className="btn btn--outline"
                        style={{ borderColor: 'var(--red)', color: 'var(--red)' }}
                      >
                        Узнать цену
                      </a>
                    ) : (
                      <Link
                        to={`/schools/${direction.school_slug}#price-list`}
                        className="btn btn--outline"
                        style={{ borderColor: 'var(--red)', color: 'var(--red)' }}
                      >
                        Узнать цену
                      </Link>
                    )}
                  </div>
                )}
              </div>
            </div>

            {coaches.length > 0 && (
              <div className="card">
                <div className="card__body">
                  <h2 className="card__title">Тренеры</h2>
                  <ul className="coach-list">
                    {coaches.map((c) => (
                      <li key={c.id}>{c.full_name}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>

          <aside className="detail-aside">
            <div className="card facility-card">
              <div className="card__body">
                <h2 className="card__title">Где проходит</h2>
                {direction.facility_name ? (
                  <>
                    <h3 className="facility-card__name">{direction.facility_name}</h3>
                    {direction.facility_address && (
                      <p className="card__text">
                        <strong>Адрес:</strong><br />
                        {direction.facility_address}
                      </p>
                    )}
                    {direction.facility_working_hours && (
                      <p className="card__text">
                        <strong>Часы работы:</strong><br />
                        {direction.facility_working_hours}
                      </p>
                    )}
                    {direction.facility_phone && (
                      <p className="card__text">
                        <strong>Телефон:</strong><br />
                        <a href={`tel:${direction.facility_phone.replace(/\s/g, '')}`}>
                          {direction.facility_phone}
                        </a>
                      </p>
                    )}
                  </>
                ) : (
                  <p className="card__text">Объект пока не указан</p>
                )}
              </div>
            </div>

            <Link to="/directions" className="btn btn--outline" style={{ width: '100%' }}>
              ← Все секции
            </Link>
          </aside>
        </div>
      </section>
    </>
  )
}
