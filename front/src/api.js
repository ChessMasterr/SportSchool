const API_BASE = import.meta.env.VITE_API_URL || '/api'

async function request(endpoint, params = {}) {
  const url = new URL(`${API_BASE}${endpoint}`, window.location.origin)
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      url.searchParams.append(key, value)
    }
  })

  const response = await fetch(url.toString())
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }
  return response.json()
}

export const api = {
  getSiteSettings: () => request('/site-settings/'),
  getSchools: () => request('/schools/'),
  getSchool: (slug) => request(`/schools/${slug}/`),
  getFacilities: (params) => request('/facilities/', params),
  getSportDirections: (params) => request('/sport-directions/', params),
  getSportDirection: (slug) => request(`/sport-directions/${slug}/`),
  getCoaches: (params) => request('/coaches/', params),
  getPrices: (params) => request('/prices/', params),
  getDocuments: (params) => request('/documents/', params),
  getNews: () => request('/news/'),
  getNewsItem: (slug) => request(`/news/${slug}/`),
  getGallery: (params) => request('/gallery/', params),
  getParents: () => request('/parents/'),
  getCompetitions: () => request('/competitions/'),
  getSchedulePeriods: (params) => request('/schedule-periods/', params),
  getSchedulePeriod: (id) => request(`/schedule-periods/${id}/`),
  getSchedule: (params) => request('/schedule/', params),
  getPoolSessions: (params) => request('/pool-sessions/', params),
  getWorkingSchedules: (params) => request('/working-schedules/', params),
  search: (q) => request('/search/', { q }),
}

export function formatTime(time) {
  if (!time) return ''
  return time.slice(0, 5)
}

export function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

export function paginateResults(data) {
  return data?.results ?? data ?? []
}
