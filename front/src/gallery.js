export const GALLERY_SECTIONS = [
  {
    key: 'training',
    title: 'Тренировки',
    text: 'Фотографии тренировочного процесса',
    icon: '🏃',
  },
  {
    key: 'competition',
    title: 'Соревнования',
    text: 'Фото с турниров и первенств — по отдельным мероприятиям',
    icon: '🏅',
  },
  {
    key: 'awards',
    title: 'Награждения',
    text: 'Церемонии награждения и достижения спортсменов',
    icon: '🏆',
  },
  {
    key: 'video',
    title: 'Видео',
    text: 'Видеозаписи тренировок, соревнований и мероприятий',
    icon: '🎬',
  },
]

export function getGallerySection(key) {
  return GALLERY_SECTIONS.find((section) => section.key === key) || null
}

export function getVideoEmbedUrl(url) {
  if (!url) return null
  try {
    const parsed = new URL(url)
    const host = parsed.hostname.replace('www.', '')
    if (host === 'youtu.be') {
      const id = parsed.pathname.split('/').filter(Boolean)[0]
      return id ? `https://www.youtube.com/embed/${id}` : null
    }
    if (host === 'youtube.com' || host === 'm.youtube.com') {
      if (parsed.pathname.startsWith('/embed/')) return url
      const id = parsed.searchParams.get('v') || parsed.pathname.split('/').filter(Boolean).pop()
      return id ? `https://www.youtube.com/embed/${id}` : null
    }
  } catch {
    return null
  }
  return null
}
