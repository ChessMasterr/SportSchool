import { useEffect, useState } from 'react'
import { api, paginateResults } from '../api'

export default function ParentsPage() {
  const [sections, setSections] = useState([])
  const [openId, setOpenId] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getParents()
      .then((data) => {
        const list = paginateResults(data)
        setSections(list)
        if (list.length) setOpenId(list[0].id)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>Родителям</h1>
          <p>Справки, правила посещения, техника безопасности, ГТО</p>
        </div>
      </div>

      <section className="section">
        <div className="container" style={{ maxWidth: 800 }}>
          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : sections.length === 0 ? (
            <div className="empty">Информация будет добавлена администратором.</div>
          ) : (
            sections.map((section) => (
              <div key={section.id} className="accordion-item">
                <button
                  className="accordion-header"
                  onClick={() => setOpenId(openId === section.id ? null : section.id)}
                >
                  {section.title}
                  <span>{openId === section.id ? '−' : '+'}</span>
                </button>
                {openId === section.id && (
                  <div
                    className="accordion-body"
                    dangerouslySetInnerHTML={{ __html: section.content }}
                  />
                )}
              </div>
            ))
          )}
        </div>
      </section>
    </>
  )
}
