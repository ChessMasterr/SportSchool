import { useEffect, useState } from 'react'
import { api, paginateResults } from '../api'

const CATEGORIES = {
  training: 'Тренировки',
  competition: 'Соревнования',
  awards: 'Награждения',
  other: 'Другое',
}

export default function GalleryPage() {
  const [images, setImages] = useState([])
  const [filter, setFilter] = useState('')
  const [lightbox, setLightbox] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    const params = filter ? { category: filter } : {}
    api.getGallery(params)
      .then((data) => setImages(paginateResults(data)))
      .catch(() => setImages([]))
      .finally(() => setLoading(false))
  }, [filter])

  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>Галерея</h1>
          <p>Фотографии тренировок, соревнований и награждений</p>
        </div>
      </div>

      <section className="section">
        <div className="container">
          <div className="filters">
            <select value={filter} onChange={(e) => setFilter(e.target.value)}>
              <option value="">Все категории</option>
              {Object.entries(CATEGORIES).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>

          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : images.length === 0 ? (
            <div className="empty">
              Фотографии будут добавлены администратором через панель управления.
            </div>
          ) : (
            <div className="gallery-grid">
              {images.map((img) => (
                <div
                  key={img.id}
                  className="gallery-item"
                  onClick={() => setLightbox(img)}
                >
                  <img src={img.image_url} alt={img.title || 'Фото'} loading="lazy" />
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {lightbox && (
        <div
          onClick={() => setLightbox(null)}
          style={{
            position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.9)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            zIndex: 1000, padding: 20, cursor: 'pointer',
          }}
        >
          <img
            src={lightbox.image_url}
            alt={lightbox.title || ''}
            style={{ maxHeight: '90vh', maxWidth: '90vw', borderRadius: 8 }}
          />
        </div>
      )}
    </>
  )
}
