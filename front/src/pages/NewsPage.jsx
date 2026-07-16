import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, formatDate, paginateResults } from '../api'

export default function NewsPage() {
  const [news, setNews] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getNews()
      .then((data) => setNews(paginateResults(data)))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>Новости</h1>
          <p>Соревнования, победы, набор в группы, мероприятия</p>
        </div>
      </div>

      <section className="section">
        <div className="container">
          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : news.length === 0 ? (
            <div className="empty">Новостей пока нет</div>
          ) : (
            <div className="grid grid--2">
              {news.map((item) => (
                <Link key={item.id} to={`/news/${item.slug}`} className="card">
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
          )}
        </div>
      </section>
    </>
  )
}
