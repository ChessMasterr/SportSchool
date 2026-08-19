import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, formatDate, paginateResults } from '../api'
import { getGallerySection } from '../gallery'

export default function GalleryCategoryPage() {
  const { category } = useParams()
  const section = getGallerySection(category)
  const [albums, setAlbums] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!section) {
      setLoading(false)
      return
    }
    setLoading(true)
    api.getGalleryAlbums({ category })
      .then((data) => setAlbums(paginateResults(data)))
      .catch(() => setAlbums([]))
      .finally(() => setLoading(false))
  }, [category, section])

  if (!section) {
    return (
      <section className="section">
        <div className="container">
          <div className="empty">Такого раздела галереи нет</div>
          <div style={{ textAlign: 'center', marginTop: 24 }}>
            <Link to="/gallery" className="btn btn--blue">К галерее</Link>
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
            <Link to="/gallery">Галерея</Link>
            {' / '}
            <span>{section.title}</span>
          </p>
          <h1>{section.icon} {section.title}</h1>
          <p>{section.text}</p>
        </div>
      </div>

      <section className="section">
        <div className="container">
          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : albums.length === 0 ? (
            <div className="empty">
              Альбомы этого раздела появятся, когда администратор добавит материалы.
            </div>
          ) : (
            <div className="grid grid--3">
              {albums.map((album) => (
                <Link
                  key={album.id}
                  to={`/gallery/${category}/${album.slug}`}
                  className="card card--link gallery-album-card"
                >
                  {album.cover_url ? (
                    <img src={album.cover_url} alt={album.title} className="card__image" />
                  ) : (
                    <div className="gallery-album-card__placeholder">
                      {section.icon}
                    </div>
                  )}
                  <div className="card__body">
                    <h2 className="card__title">{album.title}</h2>
                    {album.event_date && (
                      <p className="card__text">{formatDate(album.event_date)}</p>
                    )}
                    {album.school_name && (
                      <p className="card__text">{album.school_name}</p>
                    )}
                    <span className="tag" style={{ marginTop: 8 }}>
                      {album.items_count || 0}{' '}
                      {category === 'video' ? 'видео' : 'фото'}
                    </span>
                    <span className="card__cta">Смотреть →</span>
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
