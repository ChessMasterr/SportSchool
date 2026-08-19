import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, paginateResults } from '../api'

export default function DirectionsPage() {
  const [directions, setDirections] = useState([])
  const [schools, setSchools] = useState([])
  const [filterSchool, setFilterSchool] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api
      .getSchools()
      .then((sch) => setSchools(paginateResults(sch)))
      .catch(() => {})
  }, [])

  useEffect(() => {
    setLoading(true)
    const params = filterSchool ? { school_slug: filterSchool } : {}
    api.getSportDirections(params)
      .then((data) => setDirections(paginateResults(data)))
      .catch(() => setDirections([]))
      .finally(() => setLoading(false))
  }, [filterSchool])

  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>Секции</h1>
          <p>Выберите секцию, чтобы узнать место занятий и расписание</p>
        </div>
      </div>

      <section className="section">
        <div className="container">
          <div className="filters">
            <select
              value={filterSchool}
              onChange={(e) => setFilterSchool(e.target.value)}
            >
              <option value="">Все школы</option>
              {schools.map((s) => (
                <option key={s.id} value={s.slug}>{s.name}</option>
              ))}
            </select>
          </div>

          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : directions.length === 0 ? (
            <div className="empty">Секции не найдены</div>
          ) : (
            <div className="grid grid--2">
              {directions.map((dir) => (
                <Link
                  key={dir.id}
                  to={`/directions/${dir.slug}`}
                  className="card card--link"
                >
                  {dir.photo_url && (
                    <img src={dir.photo_url} alt={dir.name} className="card__image" />
                  )}
                  <div className="card__body">
                    <h3 className="card__title">{dir.name}</h3>
                    {dir.facility_name && (
                      <p className="card__text">
                        <strong>Где:</strong> {dir.facility_name}
                      </p>
                    )}
                    {dir.school_name && (
                      <p className="card__text">{dir.school_name}</p>
                    )}
                    {dir.age_from && (
                      <p className="card__text">
                        <strong>Возраст:</strong> {dir.age_from}
                        {dir.age_to ? `–${dir.age_to}` : '+'} лет
                      </p>
                    )}
                    {dir.level_display && (
                      <span className="tag">{dir.level_display}</span>
                    )}
                    {dir.description && (
                      <p className="card__text" style={{ marginTop: 12 }}>{dir.description}</p>
                    )}
                    <span className="card__cta">Место и расписание →</span>
                  </div>
                </Link>
              ))}
            </div>
          )}

        </div>
      </section>
    </>
  )
}
