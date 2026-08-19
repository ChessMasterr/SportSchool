import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, formatDate, paginateResults } from '../api'

export default function HomePage() {
  const [settings, setSettings] = useState(null)
  const [schools, setSchools] = useState([])
  const [facilities, setFacilities] = useState([])
  const [directions, setDirections] = useState([])
  const [news, setNews] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.getSiteSettings(),
      api.getSchools(),
      api.getFacilities(),
      api.getSportDirections(),
      api.getNews(),
    ])
      .then(([s, sch, fac, dirs, n]) => {
        setSettings(s)
        setSchools(paginateResults(sch))
        setFacilities(paginateResults(fac))
        setDirections(paginateResults(dirs))
        setNews(paginateResults(n).slice(0, 3))
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="loading">Загрузка...</div>

  const hasSectorSport = schools.some((s) => s.slug === 'sector-sporta')
  const homeSchools = hasSectorSport
    ? schools
    : [
        ...schools,
        {
          id: 'sector-sporta',
          name: 'Сектор спорта',
          short_description: 'Пока под вопросом',
          opened_date: null,
        },
      ]

  const getSchoolCover = (school) => {
    if (school?.photo_url) return school.photo_url
    const schoolId = school?.id
    if (!schoolId || facilities.length === 0) return null
    const fac = facilities.find((f) => f.school === schoolId && f.photo_url)
    return fac?.photo_url || null
  }

  return (
    <>
      <section
        className={`hero${settings?.hero_image_url ? ' hero--with-image' : ''}`}
        style={
          settings?.hero_image_url
            ? { backgroundImage: `url(${settings.hero_image_url})` }
            : undefined
        }
      >
        <div className="container hero__content">
          <h1>{settings?.hero_title || 'Спортивные школы Елабуги'}</h1>
          <p>
            {settings?.hero_subtitle ||
              'Спортивные школы и современные залы. Узнайте расписание и контакты.'}
          </p>
          <div className="hero__actions">
            <Link to="/schedule" className="btn btn--primary">Расписание</Link>
            <Link to="/contacts" className="btn btn--outline">Контакты</Link>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2 className="section__title">Наши школы</h2>
          <p className="section__subtitle">
            Спортивные школы и объекты Елабужского муниципального района
          </p>

          <div className="grid grid--4">
            {homeSchools.map((school) => (
              school.slug ? (
                <Link
                  key={school.id}
                  to={`/schools/${school.slug}`}
                  className="card card--link"
                >
                  {getSchoolCover(school) && (
                    <img
                      src={getSchoolCover(school)}
                      alt={school.name}
                      className="card__image"
                    />
                  )}
                  <div className="card__body">
                    <h3 className="card__title">{school.name}</h3>
                    <p className="card__text">{school.short_description}</p>
                    {school.opened_date && (
                      <p className="card__text" style={{ marginTop: 8 }}>
                        <span className="tag">Открыта: {formatDate(school.opened_date)}</span>
                      </p>
                    )}
                  </div>
                </Link>
              ) : (
                <div key={school.id} className="card">
                  <div className="card__body">
                    <h3 className="card__title">{school.name}</h3>
                    <p className="card__text">{school.short_description}</p>
                  </div>
                </div>
              )
            ))}
          </div>
        </div>
      </section>

      <section className="section section--alt">
        <div className="container">
          <h2 className="section__title">Преимущества</h2>
          <div className="grid grid--4">
            {[
              { icon: '🏆', title: 'Опытные тренеры', text: 'Квалифицированные тренеры-преподаватели' },
              { icon: '🏊', title: 'Современные залы', text: 'Бассейны, игровые и тренажёрные залы' },
              { icon: '🥇', title: 'Соревнования', text: 'Участие в городских и региональных соревнованиях' },
              { icon: '👨‍👩‍👧', title: 'Для всей семьи', text: 'Секции для детей и взрослых' },
            ].map((item) => (
              <div key={item.title} className="card">
                <div className="card__body" style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '2.5rem', marginBottom: 12 }}>{item.icon}</div>
                  <h3 className="card__title">{item.title}</h3>
                  <p className="card__text">{item.text}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="sections" className="section">
        <div className="container">
          <h2 className="section__title">Секции и расписание</h2>
          <p className="section__subtitle">
            Быстрый переход к видам спорта, месту занятий и расписанию
          </p>

          {directions.length === 0 ? (
            <div className="empty">Секции пока не опубликованы</div>
          ) : (
            <div className="grid grid--3">
              {directions.slice(0, 6).map((dir) => (
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
                      <span className="tag" style={{ marginTop: 8 }}>
                        {dir.age_from}{dir.age_to ? `–${dir.age_to}` : '+'} лет
                      </span>
                    )}
                    <span className="card__cta">Место и расписание →</span>
                  </div>
                </Link>
              ))}
            </div>
          )}

          <div style={{ display: 'flex', gap: 16, justifyContent: 'center', marginTop: 32, flexWrap: 'wrap' }}>
            <Link to="/directions" className="btn btn--blue">Все секции</Link>
            <Link to="/schedule" className="btn btn--outline" style={{ color: 'var(--blue)', borderColor: 'var(--blue)' }}>
              Открыть расписание
            </Link>
          </div>
        </div>
      </section>

      {news.length > 0 && (
        <section className="section">
          <div className="container">
            <h2 className="section__title">Новости</h2>
            <div className="grid grid--3">
              {news.map((item) => (
                <Link key={item.id} to={`/news/${item.slug}`} className="card card--link">
                  {item.image_url && (
                    <img src={item.image_url} alt={item.title} className="card__image" />
                  )}
                  <div className="card__body">
                    <span className="tag tag--red">{item.category_display}</span>
                    <h3 className="card__title" style={{ marginTop: 8 }}>{item.title}</h3>
                    <p className="card__text">{formatDate(item.published_at)}</p>
                  </div>
                </Link>
              ))}
            </div>
            <div style={{ textAlign: 'center', marginTop: 32 }}>
              <Link to="/news" className="btn btn--blue">Все новости</Link>
            </div>
          </div>
        </section>
      )}
    </>
  )
}
