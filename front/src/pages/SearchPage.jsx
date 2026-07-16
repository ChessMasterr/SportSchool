import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { api } from '../api'

export default function SearchPage() {
  const [params, setParams] = useSearchParams()
  const [query, setQuery] = useState(params.get('q') || '')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const q = params.get('q')
    if (q && q.length >= 2) {
      setLoading(true)
      api.search(q)
        .then(setResults)
        .catch(() => setResults(null))
        .finally(() => setLoading(false))
    }
  }, [params])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim().length >= 2) {
      setParams({ q: query.trim() })
    }
  }

  const q = params.get('q')
  const data = results?.results

  return (
    <>
      <div className="page-header">
        <div className="container">
          <h1>Поиск</h1>
        </div>
      </div>

      <section className="section">
        <div className="container" style={{ maxWidth: 800 }}>
          <form onSubmit={handleSubmit} className="filters" style={{ marginBottom: 32 }}>
            <input
              type="search"
              placeholder="Введите запрос..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={{ flex: 1, minWidth: 200 }}
            />
            <button type="submit" className="btn btn--primary">Найти</button>
          </form>

          {loading && <div className="loading">Поиск...</div>}

          {!loading && q && data && (
            <>
              {data.news?.length > 0 && (
                <div style={{ marginBottom: 32 }}>
                  <h2 className="section__title">Новости</h2>
                  {data.news.map((item) => (
                    <Link key={item.id} to={`/news/${item.slug}`} className="card" style={{ display: 'block', marginBottom: 12 }}>
                      <div className="card__body">
                        <h3 className="card__title">{item.title}</h3>
                      </div>
                    </Link>
                  ))}
                </div>
              )}

              {data.sport_directions?.length > 0 && (
                <div style={{ marginBottom: 32 }}>
                  <h2 className="section__title">Направления</h2>
                  {data.sport_directions.map((item) => (
                    <div key={item.id} className="card" style={{ marginBottom: 12 }}>
                      <div className="card__body">
                        <h3 className="card__title">{item.name}</h3>
                        <p className="card__text">{item.facility_name}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {data.coaches?.length > 0 && (
                <div style={{ marginBottom: 32 }}>
                  <h2 className="section__title">Тренеры</h2>
                  {data.coaches.map((item) => (
                    <div key={item.id} className="card" style={{ marginBottom: 12 }}>
                      <div className="card__body">
                        <h3 className="card__title">{item.full_name}</h3>
                        <p className="card__text">{item.facility_name}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {data.facilities?.length > 0 && (
                <div style={{ marginBottom: 32 }}>
                  <h2 className="section__title">Объекты</h2>
                  {data.facilities.map((item) => (
                    <div key={item.id} className="card" style={{ marginBottom: 12 }}>
                      <div className="card__body">
                        <h3 className="card__title">{item.name}</h3>
                        <p className="card__text">{item.address}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {!data.news?.length && !data.sport_directions?.length &&
               !data.coaches?.length && !data.facilities?.length && (
                <div className="empty">Ничего не найдено по запросу «{q}»</div>
              )}
            </>
          )}
        </div>
      </section>
    </>
  )
}
