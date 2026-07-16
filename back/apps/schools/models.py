from django.db import models


class School(models.Model):
    """Спортивная школа (Кама, Олимп, Юность и т.д.)."""

    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('URL-имя', unique=True)
    short_description = models.TextField('Краткое описание', blank=True)
    full_description = models.TextField('Полное описание', blank=True)
    opened_date = models.DateField('Дата открытия', null=True, blank=True)
    is_active = models.BooleanField('Активна', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Спортивная школа'
        verbose_name_plural = 'Спортивные школы'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Facility(models.Model):
    """Спортивный объект (ФОК, бассейн, зал)."""

    FACILITY_TYPES = [
        ('pool', 'Бассейн'),
        ('gym', 'Тренажёрный зал'),
        ('game_hall', 'Игровой зал'),
        ('combat_hall', 'Зал единоборств'),
        ('tennis', 'Теннисные корты'),
        ('other', 'Другое'),
    ]

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='facilities',
        verbose_name='Школа',
        null=True,
        blank=True,
    )
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('URL-имя', unique=True)
    facility_type = models.CharField(
        'Тип объекта', max_length=20, choices=FACILITY_TYPES, default='other'
    )
    address = models.CharField('Адрес', max_length=500)
    phone = models.CharField('Телефон', max_length=100, blank=True)
    phone_admin = models.CharField('Телефон администрации', max_length=100, blank=True)
    working_hours = models.CharField('Режим работы', max_length=255, blank=True)
    description = models.TextField('Описание', blank=True)
    has_hall_rental = models.BooleanField('Аренда зала', default=False)
    hall_rental_note = models.TextField('Примечание по аренде', blank=True)
    latitude = models.DecimalField(
        'Широта', max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        'Долгота', max_digits=9, decimal_places=6, null=True, blank=True
    )
    photo = models.ImageField('Фото', upload_to='facilities/', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Спортивный объект'
        verbose_name_plural = 'Спортивные объекты'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class SportDirection(models.Model):
    """Вид спорта / направление подготовки."""

    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
        ('all', 'Любой уровень'),
    ]

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='sport_directions',
        verbose_name='Школа',
        null=True,
        blank=True,
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.SET_NULL,
        related_name='sport_directions',
        verbose_name='Объект',
        null=True,
        blank=True,
    )
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('URL-имя')
    description = models.TextField('Описание', blank=True)
    age_from = models.PositiveIntegerField('Возраст от', null=True, blank=True)
    age_to = models.PositiveIntegerField('Возраст до', null=True, blank=True)
    level = models.CharField(
        'Уровень подготовки', max_length=20, choices=LEVEL_CHOICES, default='all'
    )
    requirements = models.TextField('Требования', blank=True)
    photo = models.ImageField('Фото', upload_to='sports/', blank=True)
    is_active = models.BooleanField('Активно', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Направление подготовки'
        verbose_name_plural = 'Направления подготовки'
        ordering = ['order', 'name']
        unique_together = [['school', 'slug']]

    def __str__(self):
        return self.name


class Coach(models.Model):
    """Тренер-преподаватель."""

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='coaches',
        verbose_name='Школа',
        null=True,
        blank=True,
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.SET_NULL,
        related_name='coaches',
        verbose_name='Объект',
        null=True,
        blank=True,
    )
    sport_directions = models.ManyToManyField(
        SportDirection,
        related_name='coaches',
        verbose_name='Направления',
        blank=True,
    )
    full_name = models.CharField('ФИО', max_length=255)
    photo = models.ImageField('Фото', upload_to='coaches/', blank=True)
    education = models.TextField('Образование', blank=True)
    qualification = models.TextField('Квалификация', blank=True)
    sports_titles = models.TextField('Спортивные звания', blank=True)
    experience = models.TextField('Опыт работы', blank=True)
    achievements = models.TextField('Достижения воспитанников', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренерский состав'
        ordering = ['order', 'full_name']

    def __str__(self):
        return self.full_name


class PriceItem(models.Model):
    """Позиция прейскуранта."""

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='price_items',
        verbose_name='Школа',
        null=True,
        blank=True,
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.SET_NULL,
        related_name='price_items',
        verbose_name='Объект',
        null=True,
        blank=True,
    )
    name = models.CharField('Наименование услуги', max_length=500)
    price = models.CharField('Стоимость', max_length=100)
    valid_from = models.DateField('Действует с', null=True, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Позиция прейскуранта'
        verbose_name_plural = 'Прейскурант'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name
