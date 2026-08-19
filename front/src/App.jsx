import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import AboutPage from './pages/AboutPage'
import DirectionsPage from './pages/DirectionsPage'
import DirectionDetailPage from './pages/DirectionDetailPage'
import SchoolDocumentsPage from './pages/SchoolDocumentsPage'
import CoachesPage from './pages/CoachesPage'
import SchedulePage from './pages/SchedulePage'
import NewsPage from './pages/NewsPage'
import NewsDetailPage from './pages/NewsDetailPage'
import GalleryPage from './pages/GalleryPage'
import GalleryCategoryPage from './pages/GalleryCategoryPage'
import GalleryAlbumPage from './pages/GalleryAlbumPage'
import ParentsPage from './pages/ParentsPage'
import ContactsPage from './pages/ContactsPage'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="about" element={<AboutPage />} />
        <Route path="directions" element={<DirectionsPage />} />
        <Route path="directions/:slug" element={<DirectionDetailPage />} />
        <Route path="schools/:slug" element={<SchoolDocumentsPage />} />
        <Route path="coaches" element={<CoachesPage />} />
        <Route path="schedule" element={<SchedulePage />} />
        <Route path="news" element={<NewsPage />} />
        <Route path="news/:slug" element={<NewsDetailPage />} />
        <Route path="gallery" element={<GalleryPage />} />
        <Route path="gallery/:category" element={<GalleryCategoryPage />} />
        <Route path="gallery/:category/:slug" element={<GalleryAlbumPage />} />
        <Route path="parents" element={<ParentsPage />} />
        <Route path="contacts" element={<ContactsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
