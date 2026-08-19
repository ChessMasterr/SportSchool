import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, formatDate } from '../api'
import { getGallerySection, getVideoEmbedUrl } from '../gallery'

export default function GalleryAlbumPage() {
  const { category, slug } = useParams()
  const section = getGallerySection(category)
  const [album, setAlbum] = useState(null)
  const [lightbox, setLightbox] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    setLoading(true)
    setError(false)
    api.getGalleryAlbum(slug)
      .then((data) => {
        if (category && data.category !== category) {
          setError(true)
          return
        }
        setAlbum(data)
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false))
  }, [category, slug])

  if (loading) return <div className="loading">Загрузка...</div>

  if (error || !album || !section) {
    return (
      <section className="section">
        <div className="container">
          <div className="empty">Альбом не найден</div>
          <div style={{ textAlign: 'center', marginTop: 24 }}>
            <Link to="/gallery" className="btn btn--blue">К галерее</Link>
          </div>
        </div>
      </section>
    )
  }

  const items = album.items || []

  return (
    <>
      <div className="page-header">
        <div className="container">
          <p className="breadcrumb">
            <Link to="/">Главная</Link>
            {' / '}
            <Link to="/gallery">Галерея</Link>
            {' / '}
            <Link to={`/gallery/${category}`}>{section.title}</Link>
            {' / '}
            <span>{album.title}</span>
          </p>
          <h1>{album.title}</h1>
          {album.event_date && <p>{formatDate(album.event_date)}</p>}
        </div>
      </div>

      <section className="section">
        <div className="container">
          {album.description && (
            <p className="section__subtitle">{album.description}</p>
          )}

          {items.length === 0 ? (
            <div className="empty">
              Материалы альбома будут добавлены администратором.
            </div>
          ) : (
            <div className="gallery-grid">
              {items.map((item) => {
                const isVideo = Boolean(item.video_url)
                return (
                  <button
                    type="button"
                    key={item.id}
                    className="gallery-item"
                    onClick={() => setLightbox(item)}
                  >
                    {item.image_url ? (
                      <img src={item.image_url} alt={item.title || album.title} loading="lazy" />
                    ) : (
                      <div className="gallery-item__video-stub">🎬</div>
                    )}
                    {isVideo && <span className="gallery-item__play">▶</span>}
                    {item.title && <span className="gallery-item__caption">{item.title}</span>}
                  </button>
                )
              })}
            </div>
          )}
        </div>
      </section>

      {lightbox && (
        <div className="lightbox" onClick={() => setLightbox(null)}>
          <div className="lightbox__content" onClick={(e) => e.stopPropagation()}>
            {lightbox.video_url ? (
              getVideoEmbedUrl(lightbox.video_url) ? (
                <iframe
                  title={lightbox.title || album.title}
                  src={getVideoEmbedUrl(lightbox.video_url)}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              ) : (
                <a
                  href={lightbox.video_url}
                  target="_blank"
                  rel="noreferrer"
                  className="btn btn--primary"
                >
                  Открыть видео
                </a>
              )
            ) : (
              <img src={lightbox.image_url} alt={lightbox.title || album.title} />
            )}
            {lightbox.title && <p className="lightbox__title">{lightbox.title}</p>}
          </div>
        </div>
      )}
    </>
  )
}
