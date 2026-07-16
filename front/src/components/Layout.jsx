import { useEffect, useState } from 'react'
import { Link, NavLink, Outlet } from 'react-router-dom'
import { api } from '../api'

const NAV_ITEMS = [
  { to: '/', label: 'Главная', end: true },
  { to: '/about', label: 'О школе' },
  { to: '/directions', label: 'Направления' },
  { to: '/coaches', label: 'Тренеры' },
  { to: '/schedule', label: 'Расписание' },
  { to: '/news', label: 'Новости' },
  { to: '/gallery', label: 'Галерея' },
  { to: '/parents', label: 'Родителям' },
  { to: '/contacts', label: 'Контакты' },
  { to: '/search', label: 'Поиск' },
]

export default function Layout() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [settings, setSettings] = useState(null)

  useEffect(() => {
    api.getSiteSettings().then(setSettings).catch(() => {})
  }, [])

  return (
    <div className="app-layout">
      <header className="header">
        <div className="container header__inner">
          <Link to="/" className="logo" onClick={() => setMenuOpen(false)}>
            <span className="logo__icon">⚽</span>
            <span>{settings?.site_title || 'Спортивные школы'}</span>
          </Link>

          <button
            className="burger"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Меню"
          >
            {menuOpen ? '✕' : '☰'}
          </button>

          <nav className={`nav ${menuOpen ? 'open' : ''}`}>
            {NAV_ITEMS.map(({ to, label, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) => (isActive ? 'active' : '')}
                onClick={() => setMenuOpen(false)}
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main className="main">
        <Outlet />
      </main>

      <footer className="footer">
        <div className="container">
          <div className="footer__grid">
            <div>
              <h4>{settings?.site_title || 'Спортивные школы Елабуги'}</h4>
              <p style={{ fontSize: '0.85rem' }}>
                Развитие спорта и здорового образа жизни
              </p>
            </div>
            <div>
              <h4>Разделы</h4>
              {NAV_ITEMS.slice(1, 6).map(({ to, label }) => (
                <Link key={to} to={to}>{label}</Link>
              ))}
            </div>
            <div>
              <h4>Информация</h4>
              <Link to="/parents">Родителям</Link>
              <Link to="/schedule">Расписание</Link>
              <Link to="/contacts">Контакты</Link>
            </div>
            <div>
              <h4>Контакты</h4>
              {settings?.email && (
                <a href={`mailto:${settings.email}`}>{settings.email}</a>
              )}
              {settings?.vk_url && (
                <a href={settings.vk_url} target="_blank" rel="noreferrer">ВКонтакте</a>
              )}
            </div>
          </div>
          <div className="footer__bottom">
            © {new Date().getFullYear()} Спортивные школы Елабуги. Все права защищены.
          </div>
        </div>
      </footer>
    </div>
  )
}
