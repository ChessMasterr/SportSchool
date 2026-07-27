import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import AboutPage from './pages/AboutPage'
import DirectionsPage from './pages/DirectionsPage'
import DirectionDetailPage from './pages/DirectionDetailPage'
import CoachesPage from './pages/CoachesPage'
import SchedulePage from './pages/SchedulePage'
import NewsPage from './pages/NewsPage'
import NewsDetailPage from './pages/NewsDetailPage'
import GalleryPage from './pages/GalleryPage'
import ParentsPage from './pages/ParentsPage'
import ContactsPage from './pages/ContactsPage'
import SearchPage from './pages/SearchPage'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="about" element={<AboutPage />} />
        <Route path="directions" element={<DirectionsPage />} />
        <Route path="directions/:slug" element={<DirectionDetailPage />} />
        <Route path="coaches" element={<CoachesPage />} />
        <Route path="schedule" element={<SchedulePage />} />
        <Route path="news" element={<NewsPage />} />
        <Route path="news/:slug" element={<NewsDetailPage />} />
        <Route path="gallery" element={<GalleryPage />} />
        <Route path="parents" element={<ParentsPage />} />
        <Route path="contacts" element={<ContactsPage />} />
        <Route path="search" element={<SearchPage />} />
      </Route>
    </Routes>
  )
}
