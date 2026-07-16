from django.db import models


class SchedulePeriod(models.Model):
    """Период действия расписания (например, июль 2026, учебный год 2026/27)."""

    title = models.CharField('Название', max_length=255)
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='schedule_periods',
        verbose_name='Школа',
        null=True,
        blank=True,
    )
    facility = models.ForeignKey(
        'schools.Facility',
        on_delete=models.CASCADE,
        related_name='schedule_periods',
        verbose_name='Объект',
        null=True,
        blank=True,
    )
    date_from = models.DateField('Дата начала')
    date_to = models.DateField('Дата окончания')
    is_current = models.BooleanField('Текущий период', default=False)
    note = models.TextField('Примечание', blank=True)

    class Meta:
        verbose_name = 'Период расписания'
        verbose_name_plural = 'Периоды расписания'
        ordering = ['-date_from']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_current:
            qs = SchedulePeriod.objects.filter(is_current=True)
            if self.school_id:
                qs = qs.filter(school_id=self.school_id)
            if self.facility_id:
                qs = qs.filter(facility_id=self.facility_id)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(is_current=False)
        super().save(*args, **kwargs)


class ScheduleEntry(models.Model):
    """Запись расписания занятий."""

    WEEKDAYS = [
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ]

    period = models.ForeignKey(
        SchedulePeriod,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='Период',
    )
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='schedule_entries',
        verbose_name='Школа',
        null=True,
        blank=True,
    )
    facility = models.ForeignKey(
        'schools.Facility',
        on_delete=models.CASCADE,
        related_name='schedule_entries',
        verbose_name='Объект',
    )
    sport_direction = models.ForeignKey(
        'schools.SportDirection',
        on_delete=models.SET_NULL,
        related_name='schedule_entries',
        verbose_name='Направление',
        null=True,
        blank=True,
    )
    coach = models.ForeignKey(
        'schools.Coach',
        on_delete=models.SET_NULL,
        related_name='schedule_entries',
        verbose_name='Тренер',
        null=True,
        blank=True,
    )
    weekday = models.IntegerField('День недели', choices=WEEKDAYS)
    time_start = models.TimeField('Начало')
    time_end = models.TimeField('Окончание')
    age_group = models.CharField('Возрастная группа', max_length=100, blank=True)
    group_name = models.CharField('Группа', max_length=255, blank=True)
    note = models.TextField('Примечание', blank=True)

    class Meta:
        verbose_name = 'Занятие в расписании'
        verbose_name_plural = 'Расписание занятий'
        ordering = ['weekday', 'time_start']

    def __str__(self):
        return f'{self.get_weekday_display()} {self.time_start}-{self.time_end}'


class PoolSession(models.Model):
    """Сеанс массового посещения бассейна."""

    WEEKDAYS = ScheduleEntry.WEEKDAYS

    period = models.ForeignKey(
        SchedulePeriod,
        on_delete=models.CASCADE,
        related_name='pool_sessions',
        verbose_name='Период',
    )
    facility = models.ForeignKey(
        'schools.Facility',
        on_delete=models.CASCADE,
        related_name='pool_sessions',
        verbose_name='Объект',
    )
    weekday = models.IntegerField('День недели', choices=WEEKDAYS)
    time_start = models.TimeField('Начало')
    time_end = models.TimeField('Окончание')
    session_type = models.CharField(
        'Тип сеанса',
        max_length=100,
        blank=True,
        help_text='Например: детский, взрослый, свободное плавание',
    )
    note = models.TextField('Примечание', blank=True)

    class Meta:
        verbose_name = 'Сеанс бассейна'
        verbose_name_plural = 'Сеансы бассейна'
        ordering = ['weekday', 'time_start']

    def __str__(self):
        return f'{self.get_weekday_display()} {self.time_start}-{self.time_end}'


class FacilityWorkingSchedule(models.Model):
    """График работы объекта (тренажёрный зал с инструктором и т.д.)."""

    SCHEDULE_TYPES = [
        ('general', 'Общий режим работы'),
        ('instructor', 'С инструктором'),
        ('break', 'Перерыв'),
    ]

    facility = models.ForeignKey(
        'schools.Facility',
        on_delete=models.CASCADE,
        related_name='working_schedules',
        verbose_name='Объект',
    )
    schedule_type = models.CharField(
        'Тип', max_length=20, choices=SCHEDULE_TYPES, default='general'
    )
    weekday = models.IntegerField(
        'День недели',
        choices=ScheduleEntry.WEEKDAYS,
        null=True,
        blank=True,
        help_text='Пусто — ежедневно',
    )
    time_start = models.TimeField('Начало')
    time_end = models.TimeField('Окончание')
    note = models.TextField('Примечание', blank=True)

    class Meta:
        verbose_name = 'График работы объекта'
        verbose_name_plural = 'Графики работы объектов'
        ordering = ['facility', 'schedule_type', 'weekday', 'time_start']

    def __str__(self):
        day = self.get_weekday_display() if self.weekday is not None else 'Ежедневно'
        return f'{self.facility.name}: {day} {self.time_start}-{self.time_end}'
