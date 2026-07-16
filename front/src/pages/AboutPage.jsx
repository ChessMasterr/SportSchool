import { useEffect, useState } from 'react'
import { api, paginateResults } from '../api'

const DOC_GROUPS = {
  license: 'Лицензии и сертификаты',
  charter: 'Устав',
  personal_data: 'Персональные данные',
  consent: 'Согласие на обработку данных',
  privacy: 'Политика конфиденциальности',
  admission: 'Правила приёма',
  achievement: 'Достижения',
  other: 'Другие документы',
}

export default function AboutPage() {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getDocuments()
      .then((data) => setDocuments(paginateResults(data)))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const grouped = documents.reduce((acc, doc) => {
    const key = doc.doc_type || 'other'
    if (!acc[key]) acc[key] = []
    acc[key].push(doc)
    return acc
  }, {})

  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>О школе</h1>
          <p>Документы, лицензии, достижения и правила</p>
        </div>
      </div>

      <section className="section">
        <div className="container">
          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : Object.keys(grouped).length === 0 ? (
            <div className="empty">
              <p>Документы будут добавлены администратором через панель управления.</p>
            </div>
          ) : (
            Object.entries(grouped).map(([type, docs]) => (
              <div key={type} style={{ marginBottom: 40 }}>
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
                            style={{ marginTop: 12, fontSize: '0.85rem', padding: '8px 16px' }}
                          >
                            Скачать документ
                          </a>
                        ) : doc.content ? (
                          <div
                            className="card__text"
                            dangerouslySetInnerHTML={{ __html: doc.content }}
                          />
                        ) : null}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      </section>
    </>
  )
}
