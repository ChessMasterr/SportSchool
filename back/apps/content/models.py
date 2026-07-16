from django.db import models


class SiteSettings(models.Model):
    """Глобальные настройки сайта (singleton)."""

    site_title = models.CharField('Название сайта', max_length=255, default='Спортивные школы Елабуги')
    hero_title = models.CharField('Заголовок на главной', max_length=500, blank=True)
    hero_subtitle = models.TextField('Подзаголовок на главной', blank=True)
    hero_image = models.ImageField('Баннер главной', upload_to='site/', blank=True)
    email = models.EmailField('E-mail', blank=True)
    vk_url = models.URLField('ВКонтакте', blank=True)
    telegram_url = models.URLField('Telegram', blank=True)
    price_list_file = models.FileField(
        'Файл прейскуранта (аренда)', upload_to='documents/', blank=True
    )

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.site_title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Document(models.Model):
    """Документы (лицензии, устав, политики)."""

    DOC_TYPES = [
        ('license', 'Лицензия / сертификат'),
        ('charter', 'Устав'),
        ('personal_data', 'Положение о персональных данных'),
        ('consent', 'Согласие на обработку данных'),
        ('privacy', 'Политика конфиденциальности'),
        ('admission', 'Правила приёма'),
        ('achievement', 'Достижения'),
        ('other', 'Другое'),
    ]

    title = models.CharField('Название', max_length=255)
    doc_type = models.CharField('Тип', max_length=20, choices=DOC_TYPES, default='other')
    file = models.FileField('Файл', upload_to='documents/', blank=True)
    content = models.TextField('Текст', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_published = models.BooleanField('Опубликован', default=True)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class News(models.Model):
    """Новости."""

    CATEGORY_CHOICES = [
        ('competition', 'Соревнования'),
        ('victory', 'Победы'),
        ('recruitment', 'Набор в группы'),
        ('event', 'Мероприятия'),
        ('other', 'Другое'),
    ]

    title = models.CharField('Заголовок', max_length=500)
    slug = models.SlugField('URL-имя', unique=True)
    body = models.TextField('Текст')
    category = models.CharField(
        'Категория', max_length=20, choices=CATEGORY_CHOICES, default='other'
    )
    image = models.ImageField('Фото', upload_to='news/', blank=True)
    video_url = models.URLField('Видео (URL)', blank=True)
    published_at = models.DateTimeField('Дата публикации')
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    """Фотографии галереи."""

    CATEGORY_CHOICES = [
        ('training', 'Тренировки'),
        ('competition', 'Соревнования'),
        ('awards', 'Награждения'),
        ('other', 'Другое'),
    ]

    title = models.CharField('Название', max_length=255, blank=True)
    image = models.ImageField('Фото', upload_to='gallery/')
    category = models.CharField(
        'Категория', max_length=20, choices=CATEGORY_CHOICES, default='other'
    )
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Школа',
    )
    order = models.PositiveIntegerField('Порядок', default=0)
    is_published = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Фото галереи'
        verbose_name_plural = 'Галерея'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title or f'Фото #{self.pk}'


class ParentInfo(models.Model):
    """Информация для родителей."""

    SECTION_CHOICES = [
        ('equipment', 'Что взять на тренировку'),
        ('medical', 'Медицинские справки'),
        ('rules', 'Правила посещения'),
        ('safety', 'Техника безопасности'),
        ('faq', 'Частые вопросы'),
        ('gto', 'ГТО'),
        ('pool_rules', 'Правила бассейна'),
    ]

    section = models.CharField('Раздел', max_length=20, choices=SECTION_CHOICES, unique=True)
    title = models.CharField('Заголовок', max_length=255)
    content = models.TextField('Содержание')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Информация для родителей'
        verbose_name_plural = 'Родителям'
        ordering = ['order']

    def __str__(self):
        return self.title


class CompetitionEvent(models.Model):
    """Календарь соревнований."""

    title = models.CharField('Название', max_length=500)
    description = models.TextField('Описание', blank=True)
    event_date = models.DateField('Дата')
    location = models.CharField('Место', max_length=500, blank=True)
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Школа',
    )
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Календарь соревнований'
        ordering = ['event_date']

    def __str__(self):
        return f'{self.title} ({self.event_date})'
