import { Link } from 'react-router-dom'
import { GALLERY_SECTIONS } from '../gallery'

export default function GalleryPage() {
  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>Галерея</h1>
          <p>Фотографии тренировок, соревнований, награждений и видео</p>
        </div>
      </div>

      <section className="section">
        <div className="container">
          <div className="grid grid--2">
            {GALLERY_SECTIONS.map((section) => (
              <Link
                key={section.key}
                to={`/gallery/${section.key}`}
                className="card card--link gallery-section-card"
              >
                <div className="card__body">
                  <span className="gallery-section-card__icon">{section.icon}</span>
                  <h2 className="card__title">{section.title}</h2>
                  <p className="card__text">{section.text}</p>
                  <span className="card__cta">Открыть раздел →</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </>
  )
}
