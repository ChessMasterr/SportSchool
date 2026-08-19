import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, paginateResults } from '../api'

const DOC_GROUPS = {
  license: 'Лицензии и сертификаты',
  charter: 'Устав',
  personal_data: 'Персональные данные',
  consent: 'Согласие на обработку данных',
  privacy: 'Политика конфиденциальности',
  admission: 'Правила приёма',
  achievement: 'Достижения',
  price_list: 'Прейскурант',
  other: 'Другие документы',
}

export default function SchoolDocumentsPage() {
  const { slug } = useParams()
  const [school, setSchool] = useState(null)
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    setLoading(true)
    setError(false)

    Promise.all([
      api.getSchool(slug),
      api.getDocuments({ school_slug: slug }),
    ])
      .then(([sch, docs]) => {
        setSchool(sch)
        setDocuments(paginateResults(docs))
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false))
  }, [slug])

  const grouped = useMemo(() => {
    return documents.reduce((acc, doc) => {
      const key = doc.doc_type || 'other'
      if (!acc[key]) acc[key] = []
      acc[key].push(doc)
      return acc
    }, {})
  }, [documents])

  if (loading) return <div className="loading">Загрузка...</div>

  if (error || !school) {
    return (
      <section className="section">
        <div className="container">
          <div className="empty">Школа не найдена</div>
          <div style={{ textAlign: 'center', marginTop: 24 }}>
            <Link to="/directions" className="btn btn--blue">
              К секциям
            </Link>
          </div>
        </div>
      </section>
    )
  }

  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>{school.name}</h1>
          <p>Документы и материалы по школе</p>
        </div>
      </div>

      <section className="section">
        <div className="container">
          {Object.keys(grouped).length === 0 ? (
            <div className="empty">
              Документы будут добавлены администратором через панель управления.
            </div>
          ) : (
            Object.entries(grouped).map(([type, docs]) => {
              const isPrice = type === 'price_list'
              return (
                <div key={type} style={{ marginBottom: 40 }} id={isPrice ? 'price-list' : undefined}>
                  <h2 className="section__title">{DOC_GROUPS[type] || type}</h2>
                  <div className="grid grid--2">
                    {docs.map((doc) => (
                      <div key={doc.id} className="card">
                        <div className="card__body">
                          <h3 className="card__title">{doc.title}</h3>

                          {doc.file_url ? (
                            <a
                              href={doc.file_url}
                              target="_blank"
                              rel="noreferrer"
                              className="btn btn--blue"
                              style={{
                                marginTop: 12,
                                fontSize: '0.85rem',
                                padding: '8px 16px',
                              }}
                            >
                              Скачать документ
                            </a>
                          ) : isPrice ? (
                            <div className="empty" style={{ marginTop: 12 }}>
                              Файл прейскуранта не прикреплён
                            </div>
                          ) : doc.content ? (
                            <div
                              className="card__text"
                              style={{ marginTop: 12 }}
                              dangerouslySetInnerHTML={{ __html: doc.content }}
                            />
                          ) : null}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })
          )}

          <div style={{ textAlign: 'center', marginTop: 32 }}>
            <Link to="/directions" className="btn btn--outline">
              ← К секциям
            </Link>
          </div>
        </div>
      </section>
    </>
  )
}

