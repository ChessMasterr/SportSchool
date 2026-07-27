import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, formatDate, paginateResults } from '../api'

export default function HomePage() {
  const [settings, setSettings] = useState(null)
  const [directions, setDirections] = useState([])
  const [news, setNews] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.getSiteSettings(),
      api.getSportDirections(),
      api.getNews(),
    ])
      .then(([s, dirs, n]) => {
        setSettings(s)
        setDirections(paginateResults(dirs))
        setNews(paginateResults(n).slice(0, 3))
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="loading">Загрузка...</div>

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
              'Выберите секцию — узнайте, где проходят занятия, и посмотрите расписание.'}
          </p>
          <div className="hero__actions">
            <a href="#sections" className="btn btn--primary">Выбрать секцию</a>
            <Link to="/contacts" className="btn btn--outline">Контакты</Link>
          </div>
        </div>
      </section>

      <section id="sections" className="section">
        <div className="container">
          <h2 className="section__title">Секции</h2>
          <p className="section__subtitle">
            Выберите вид спорта: место занятий и расписание откроются на странице секции
          </p>

          {directions.length === 0 ? (
            <div className="empty">Секции пока не опубликованы</div>
          ) : (
            <div className="grid grid--3">
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

          <div style={{ textAlign: 'center', marginTop: 32 }}>
            <Link to="/directions" className="btn btn--blue">Все секции</Link>
          </div>
        </div>
      </section>

      <section className="section section--alt">
        <div className="container">
          <h2 className="section__title">Как это работает</h2>
          <div className="grid grid--3">
            {[
              {
                step: '1',
                title: 'Выберите секцию',
                text: 'Найдите нужный вид спорта в списке секций',
              },
              {
                step: '2',
                title: 'Узнайте место',
                text: 'Посмотрите объект, адрес, телефон и часы работы',
              },
              {
                step: '3',
                title: 'Смотрите расписание',
                text: 'Откройте дни и время занятий именно по этой секции',
              },
            ].map((item) => (
              <div key={item.step} className="card">
                <div className="card__body">
                  <span className="step-badge">{item.step}</span>
                  <h3 className="card__title">{item.title}</h3>
                  <p className="card__text">{item.text}</p>
                </div>
              </div>
            ))}
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
