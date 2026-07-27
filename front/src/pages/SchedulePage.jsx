import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api, formatTime, paginateResults } from '../api'

export default function SchedulePage() {
  const [searchParams] = useSearchParams()
  const [tab, setTab] = useState('classes')
  const [schools, setSchools] = useState([])
  const [facilities, setFacilities] = useState([])
  const [periods, setPeriods] = useState([])
  const [schedule, setSchedule] = useState([])
  const [poolSessions, setPoolSessions] = useState([])
  const [workingSchedules, setWorkingSchedules] = useState([])

  const [filterSchool, setFilterSchool] = useState('')
  const [filterFacility, setFilterFacility] = useState('')
  const [filterSport, setFilterSport] = useState(searchParams.get('sport') || '')
  const [sports, setSports] = useState([])
  const [loading, setLoading] = useState(true)
  const [currentPeriod, setCurrentPeriod] = useState(null)

  useEffect(() => {
    const sport = searchParams.get('sport')
    if (sport) setFilterSport(sport)
  }, [searchParams])

  useEffect(() => {
    Promise.all([api.getSchools(), api.getFacilities(), api.getSportDirections()])
      .then(([sch, fac, sp]) => {
        setSchools(paginateResults(sch))
        setFacilities(paginateResults(fac))
        setSports(paginateResults(sp))
      })
      .catch(() => {})
  }, [])

  useEffect(() => {
    const params = { is_current: true }
    if (filterSchool) params.school_slug = filterSchool
    if (filterFacility) params.facility = filterFacility

    api.getSchedulePeriods(params)
      .then((data) => {
        const list = paginateResults(data)
        setPeriods(list)
        setCurrentPeriod(list[0] || null)
      })
      .catch(() => setPeriods([]))
  }, [filterSchool, filterFacility])

  useEffect(() => {
    setLoading(true)
    const params = {}
    if (filterSchool) params.school_slug = filterSchool
    if (filterFacility) params.facility = filterFacility
    if (filterSport) params.sport_direction = filterSport
    if (currentPeriod) params.period = currentPeriod.id

    Promise.all([
      api.getSchedule(params),
      api.getPoolSessions(params),
      api.getWorkingSchedules(filterFacility ? { facility: filterFacility } : {}),
    ])
      .then(([sch, pool, work]) => {
        setSchedule(paginateResults(sch))
        setPoolSessions(paginateResults(pool))
        setWorkingSchedules(paginateResults(work))
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [filterSchool, filterFacility, filterSport, currentPeriod])

  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>Расписание</h1>
          <p>Занятия, сеансы бассейна и график работы объектов</p>
        </div>
      </div>

      <section className="section">
        <div className="container">
          {currentPeriod?.note && (
            <div className="notice">{currentPeriod.note}</div>
          )}

          {currentPeriod && (
            <p style={{ marginBottom: 20, color: 'var(--gray-600)' }}>
              <strong>Период:</strong> {currentPeriod.title}
              {' '}({currentPeriod.date_from} — {currentPeriod.date_to})
            </p>
          )}

          <div className="filters">
            <select value={filterSchool} onChange={(e) => setFilterSchool(e.target.value)}>
              <option value="">Все школы</option>
              {schools.map((s) => (
                <option key={s.id} value={s.slug}>{s.name}</option>
              ))}
            </select>
            <select value={filterFacility} onChange={(e) => setFilterFacility(e.target.value)}>
              <option value="">Все объекты</option>
              {facilities.map((f) => (
                <option key={f.id} value={f.id}>{f.name}</option>
              ))}
            </select>
            <select value={filterSport} onChange={(e) => setFilterSport(e.target.value)}>
              <option value="">Все виды спорта</option>
              {sports.map((s) => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
            {periods.length > 1 && (
              <select
                value={currentPeriod?.id || ''}
                onChange={(e) => {
                  const p = periods.find((x) => x.id === Number(e.target.value))
                  setCurrentPeriod(p)
                }}
              >
                {periods.map((p) => (
                  <option key={p.id} value={p.id}>{p.title}</option>
                ))}
              </select>
            )}
          </div>

          <div style={{ display: 'flex', gap: 8, marginBottom: 24, flexWrap: 'wrap' }}>
            {[
              { id: 'classes', label: 'Занятия' },
              { id: 'pool', label: 'Сеансы бассейна' },
              { id: 'working', label: 'График работы' },
            ].map(({ id, label }) => (
              <button
                key={id}
                className={`btn ${tab === id ? 'btn--primary' : 'btn--blue'}`}
                onClick={() => setTab(id)}
                style={tab !== id ? { background: 'var(--gray-200)', color: 'var(--gray-800)', borderColor: 'var(--gray-200)' } : {}}
              >
                {label}
              </button>
            ))}
          </div>

          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : tab === 'classes' ? (
            schedule.length === 0 ? (
              <div className="empty">
                Расписание занятий будет опубликовано с 1 сентября. Выберите другой объект или период.
              </div>
            ) : (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>День</th>
                      <th>Время</th>
                      <th>Направление</th>
                      <th>Тренер</th>
                      <th>Группа</th>
                      <th>Объект</th>
                    </tr>
                  </thead>
                  <tbody>
                    {schedule.map((row) => (
                      <tr key={row.id}>
                        <td>{row.weekday_display}</td>
                        <td>{formatTime(row.time_start)} – {formatTime(row.time_end)}</td>
                        <td>{row.sport_name || '—'}</td>
                        <td>{row.coach_name || '—'}</td>
                        <td>{row.age_group || row.group_name || '—'}</td>
                        <td>{row.facility_name}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )
          ) : tab === 'pool' ? (
            poolSessions.length === 0 ? (
              <div className="empty">Сеансы бассейна не найдены для выбранных фильтров.</div>
            ) : (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>День</th>
                      <th>Время</th>
                      <th>Тип сеанса</th>
                      <th>Объект</th>
                      <th>Примечание</th>
                    </tr>
                  </thead>
                  <tbody>
                    {poolSessions.map((row) => (
                      <tr key={row.id}>
                        <td>{row.weekday_display}</td>
                        <td>{formatTime(row.time_start)} – {formatTime(row.time_end)}</td>
                        <td>{row.session_type || '—'}</td>
                        <td>{row.facility_name}</td>
                        <td>{row.note || '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )
          ) : (
            workingSchedules.length === 0 ? (
              <div className="empty">График работы не найден.</div>
            ) : (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Объект</th>
                      <th>Тип</th>
                      <th>День</th>
                      <th>Время</th>
                      <th>Примечание</th>
                    </tr>
                  </thead>
                  <tbody>
                    {workingSchedules.map((row) => (
                      <tr key={row.id}>
                        <td>{row.facility_name}</td>
                        <td>{row.schedule_type_display}</td>
                        <td>{row.weekday_display}</td>
                        <td>{formatTime(row.time_start)} – {formatTime(row.time_end)}</td>
                        <td>{row.note || '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )
          )}
        </div>
      </section>
    </>
  )
}
