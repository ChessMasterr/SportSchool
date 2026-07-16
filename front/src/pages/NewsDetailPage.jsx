import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, formatDate } from '../api'

export default function NewsDetailPage() {
  const { slug } = useParams()
  const [item, setItem] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    api.getNewsItem(slug)
      .then(setItem)
      .catch(() => setError(true))
      .finally(() => setLoading(false))
  }, [slug])

  if (loading) return <div className="loading">Загрузка...</div>
  if (error || !item) {
    return (
      <div className="empty">
        <p>Новость не найдена</p>
        <Link to="/news" className="btn btn--blue" style={{ marginTop: 16 }}>К списку новостей</Link>
      </div>
    )
  }

  return (
    <>
      <div className="page-header">
        <div className="container">
          <span className="tag tag--red">{item.category_display}</span>
          <h1 style={{ marginTop: 12 }}>{item.title}</h1>
          <p>{formatDate(item.published_at)}</p>
        </div>
      </div>

      <section className="section">
        <div className="container" style={{ maxWidth: 800 }}>
          {item.image_url && (
            <img
              src={item.image_url}
              alt={item.title}
              style={{ borderRadius: 'var(--radius)', marginBottom: 24, width: '100%' }}
            />
          )}
          <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>{item.body}</div>
          {item.video_url && (
            <div style={{ marginTop: 24 }}>
              <a href={item.video_url} target="_blank" rel="noreferrer" className="btn btn--blue">
                Смотреть видео
              </a>
            </div>
          )}
          <div style={{ marginTop: 40 }}>
            <Link to="/news" className="btn btn--blue">← Все новости</Link>
          </div>
        </div>
      </section>
    </>
  )
}
