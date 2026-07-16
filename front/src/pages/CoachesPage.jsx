import { useEffect, useState } from 'react'
import { api, paginateResults } from '../api'

export default function CoachesPage() {
  const [coaches, setCoaches] = useState([])
  const [facilities, setFacilities] = useState([])
  const [filterFacility, setFilterFacility] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getFacilities()
      .then((data) => setFacilities(paginateResults(data)))
      .catch(() => {})
  }, [])

  useEffect(() => {
    setLoading(true)
    const params = filterFacility ? { facility: filterFacility } : {}
    api.getCoaches(params)
      .then((data) => setCoaches(paginateResults(data)))
      .catch(() => setCoaches([]))
      .finally(() => setLoading(false))
  }, [filterFacility])

  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>Тренерский состав</h1>
          <p>Тренеры-преподаватели по объектам</p>
        </div>
      </div>

      <section className="section">
        <div className="container">
          <div className="filters">
            <select
              value={filterFacility}
              onChange={(e) => setFilterFacility(e.target.value)}
            >
              <option value="">Все объекты</option>
              {facilities.map((f) => (
                <option key={f.id} value={f.id}>{f.name}</option>
              ))}
            </select>
          </div>

          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : coaches.length === 0 ? (
            <div className="empty">
              <p>Информация о тренерах будет добавлена администратором.</p>
            </div>
          ) : (
            <div className="grid grid--3">
              {coaches.map((coach) => (
                <div key={coach.id} className="card coach-card">
                  {coach.photo_url ? (
                    <img src={coach.photo_url} alt={coach.full_name} className="coach-card__photo" />
                  ) : (
                    <div className="coach-card__photo" style={{
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontSize: '3rem', color: 'var(--blue)',
                    }}>👤</div>
                  )}
                  <h3 className="coach-card__name">{coach.full_name}</h3>
                  {coach.facility_name && (
                    <p className="coach-card__role">{coach.facility_name}</p>
                  )}
                  {coach.sport_directions_list?.length > 0 && (
                    <p className="card__text">
                      {coach.sport_directions_list.join(', ')}
                    </p>
                  )}
                  {coach.education && (
                    <p className="card__text" style={{ marginTop: 8 }}>
                      <strong>Образование:</strong> {coach.education}
                    </p>
                  )}
                  {coach.qualification && (
                    <p className="card__text">
                      <strong>Квалификация:</strong> {coach.qualification}
                    </p>
                  )}
                  {coach.sports_titles && (
                    <p className="card__text">
                      <strong>Звания:</strong> {coach.sports_titles}
                    </p>
                  )}
                  {coach.experience && (
                    <p className="card__text">
                      <strong>Опыт:</strong> {coach.experience}
                    </p>
                  )}
                  {coach.achievements && (
                    <p className="card__text">
                      <strong>Достижения воспитанников:</strong> {coach.achievements}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </>
  )
}
