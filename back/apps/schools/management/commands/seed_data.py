from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.content.models import GalleryImage, News, ParentInfo, SiteSettings
from apps.schedules.models import FacilityWorkingSchedule, PoolSession, ScheduleEntry, SchedulePeriod
from apps.schools.models import Coach, Facility, PriceItem, School, SportDirection


class Command(BaseCommand):
    help = 'Загрузка начальных данных для сайта спортивных школ'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка начальных данных...')

        settings = SiteSettings.load()
        settings.site_title = 'Спортивные школы Елабуги'
        settings.hero_title = 'Спортивные школы Елабуги'
        settings.hero_subtitle = (
            'Профессиональные тренеры, современные залы, участие в соревнованиях. '
            'Развивайте спортивный потенциал вашего ребёнка вместе с нами!'
        )
        settings.email = 'sport@elabuga.ru'
        settings.save()

        kama, _ = School.objects.update_or_create(
            slug='kama',
            defaults={
                'name': 'МБУ ДО «СШ «Кама» ЕМР РТ',
                'short_description': (
                    'Спортивная школа «Кама» — плавание для детей от 7 до 18 лет. '
                    '5 тренеров-преподавателей. Открыта с 01.12.2023.'
                ),
                'full_description': (
                    'МБУ ДО «Спортивная школа «Кама» Елабужского муниципального района '
                    'Республики Татарстан» расположена в СК «Единая Россия». '
                    'Основное направление — плавание. Возраст обучающихся с 7 до 18 лет.'
                ),
                'opened_date': '2023-12-01',
                'order': 1,
            },
        )

        for slug, name, desc, order in [
            ('olymp', 'СШ «Олимп»', 'Спортивная школа «Олимп»', 2),
            ('yunost', 'СШ «Юность»', 'Спортивная школа «Юность»', 3),
        ]:
            School.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'short_description': desc,
                    'order': order,
                    'is_active': True,
                },
            )

        facilities_data = [
            {
                'slug': 'kama-pool',
                'school': kama,
                'name': 'СШ «Кама» — бассейн',
                'facility_type': 'pool',
                'address': '423602, РТ, г. Елабуга, ул. Тази Гиззата, д. 31, СК «Единая Россия»',
                'phone': '8 (85557) 3-47-17',
                'working_hours': '8:00 — 21:00',
                'description': (
                    'Плавательный бассейн. Секция плавания (5 тренеров-преподавателей). '
                    'Посещение по расписанию сеансов с 7 лет. '
                    'До 12 лет включительно нужна справка, с 12 лет справка не требуется.'
                ),
                'order': 1,
            },
            {
                'slug': 'tanayka',
                'school': None,
                'name': 'ФОК «Танайка»',
                'facility_type': 'game_hall',
                'address': 'РТ, Елабужский район, с. Танайка, ул. Ермазова, д. 8',
                'phone': '8 (85557) 3-06-72',
                'working_hours': '8:00 — 22:00',
                'has_hall_rental': True,
                'hall_rental_note': 'Возможна аренда игрового зала. Для записи звоните по указанному телефону.',
                'order': 2,
            },
            {
                'slug': 'khlystovo',
                'school': None,
                'name': 'ФОК «Хлыстово»',
                'facility_type': 'other',
                'address': 'РТ, Елабужский район, с. Хлыстово, ул. Энергетиков, д. 1',
                'phone': '+7 (85557) 7-78-15',
                'working_hours': '8:50 — 21:00',
                'description': 'Бассейн, игровой зал и тренажёрный зал.',
                'has_hall_rental': True,
                'hall_rental_note': 'Возможна аренда игрового зала. Для записи звоните по указанному телефону.',
                'order': 3,
            },
            {
                'slug': 'chempion',
                'school': None,
                'name': 'ФОК «Чемпион»',
                'facility_type': 'other',
                'address': 'г. Елабуга, проспект Мира, д. 4',
                'phone': '8 (85557) 3-43-34',
                'phone_admin': '8 (85557) 3-42-35',
                'working_hours': '7:30 — 21:00',
                'description': 'Игровой зал, тренажёрный зал, открытые теннисные корты, бассейн.',
                'has_hall_rental': True,
                'hall_rental_note': 'Возможна аренда игрового зала. Для записи звоните по указанному телефону.',
                'order': 4,
            },
            {
                'slug': 'lider',
                'school': None,
                'name': 'Зал единоборств «Лидер»',
                'facility_type': 'combat_hall',
                'address': 'г. Елабуга, ул. Строителей, д. 9а',
                'phone': '+7 (85557) 3-25-74',
                'working_hours': '8:00 — 21:00',
                'description': 'Тренажёрный зал. Расписание как у объекта, инструктор отсутствует.',
                'order': 5,
            },
        ]

        facilities = {}
        for data in facilities_data:
            slug = data.pop('slug')
            school = data.pop('school', None)
            fac, _ = Facility.objects.update_or_create(
                slug=slug,
                defaults={**data, 'school': school},
            )
            facilities[slug] = fac

        swimming, _ = SportDirection.objects.update_or_create(
            school=kama,
            slug='plavanie',
            defaults={
                'facility': facilities['kama-pool'],
                'name': 'Плавание',
                'description': (
                    'Секция плавания. 5 тренеров-преподавателей. '
                    'Возраст обучающихся с 7 до 18 лет.'
                ),
                'age_from': 7,
                'age_to': 18,
                'requirements': (
                    'До 12 лет включительно необходима медицинская справка. '
                    'С 12 лет справка не требуется.'
                ),
                'order': 1,
            },
        )

        combat_sports = [
            'Бокс', 'Дзюдо', 'Тхэквондо', 'Вольная борьба', 'Борьба на поясах',
            'Корэш', 'Баскетбол', 'Тяжёлая атлетика', 'Пауэрлифтинг', 'Настольный теннис',
        ]
        for i, sport in enumerate(combat_sports):
            SportDirection.objects.update_or_create(
                school=None,
                slug=sport.lower().replace(' ', '-').replace('ё', 'e'),
                defaults={
                    'facility': facilities['lider'],
                    'name': sport,
                    'description': f'Секция «{sport}». Расписание будет обновлено с 1 сентября.',
                    'order': i + 2,
                },
            )

        prices = [
            ('Разовое посещение для детей (7–17 лет) без сауны / с сауной', '160 / 200'),
            ('Разовое посещение для взрослых (18+) без сауны / с сауной', '200 / 230'),
            ('Детский абонемент (до 17 лет) на 12 посещений', '2000'),
            ('Взрослый абонемент (18+) на 12 посещений', '2300'),
            ('Плавательный бассейн без сауны — 6 дорожек (50–55 чел.)', '7500'),
            ('Плавательный бассейн с сауной — 6 дорожек (50–55 чел.)', '8600'),
            ('Плавательный бассейн без сауны — 1 дорожка (6–8 чел.)', '1600'),
            ('Плавательный бассейн с сауной — 1 дорожка (6–8 чел.)', '1900'),
            ('Бассейн с сауной, комната отдыха (до 6 чел.) за час', '8000'),
            ('Абонемент с тренером (8 занятий в месяц)', '3000'),
            ('Зал хореографии до 16:00 / с 16:00', '450 / 550'),
            ('Индивидуальное занятие с тренером (45 мин.)', '700'),
        ]
        for i, (name, price) in enumerate(prices):
            PriceItem.objects.update_or_create(
                school=kama,
                name=name,
                defaults={'price': price, 'facility': facilities['kama-pool'], 'order': i + 1},
            )

        period, _ = SchedulePeriod.objects.update_or_create(
            title='Июль 2026',
            school=kama,
            facility=facilities['kama-pool'],
            defaults={
                'date_from': '2026-07-01',
                'date_to': '2026-07-31',
                'is_current': True,
                'note': 'С августа 2026 расписание изменится в связи с началом учебного процесса.',
            },
        )

        if not ScheduleEntry.objects.filter(period=period).exists():
            sample_sessions = [
                (0, '09:00', '10:00', '7–10 лет'),
                (0, '10:30', '11:30', '11–14 лет'),
                (2, '09:00', '10:00', '7–10 лет'),
                (2, '10:30', '11:30', '15–18 лет'),
                (4, '09:00', '10:00', '11–14 лет'),
                (4, '16:00', '17:00', '7–10 лет'),
            ]
            for weekday, t_start, t_end, age in sample_sessions:
                ScheduleEntry.objects.create(
                    period=period,
                    school=kama,
                    facility=facilities['kama-pool'],
                    sport_direction=swimming,
                    weekday=weekday,
                    time_start=t_start,
                    time_end=t_end,
                    age_group=age,
                )

        if not PoolSession.objects.filter(period=period).exists():
            pool_times = [
                (0, '07:00', '08:00', 'Утренний сеанс'),
                (0, '18:00', '19:30', 'Вечерний сеанс'),
                (5, '10:00', '12:00', 'Выходной день — свободное плавание'),
            ]
            for weekday, t_start, t_end, stype in pool_times:
                PoolSession.objects.create(
                    period=period,
                    facility=facilities['kama-pool'],
                    weekday=weekday,
                    time_start=t_start,
                    time_end=t_end,
                    session_type=stype,
                )

        chempion = facilities['chempion']
        if not FacilityWorkingSchedule.objects.filter(facility=chempion).exists():
            FacilityWorkingSchedule.objects.bulk_create([
                FacilityWorkingSchedule(
                    facility=chempion, schedule_type='general',
                    weekday=None, time_start='07:30', time_end='21:00',
                    note='Ежедневно',
                ),
                FacilityWorkingSchedule(
                    facility=chempion, schedule_type='instructor',
                    weekday=0, time_start='14:00', time_end='21:00',
                ),
                FacilityWorkingSchedule(
                    facility=chempion, schedule_type='instructor',
                    weekday=1, time_start='14:00', time_end='21:00',
                ),
                FacilityWorkingSchedule(
                    facility=chempion, schedule_type='instructor',
                    weekday=2, time_start='14:00', time_end='21:00',
                ),
                FacilityWorkingSchedule(
                    facility=chempion, schedule_type='instructor',
                    weekday=3, time_start='14:00', time_end='21:00',
                ),
                FacilityWorkingSchedule(
                    facility=chempion, schedule_type='instructor',
                    weekday=4, time_start='14:00', time_end='21:00',
                ),
                FacilityWorkingSchedule(
                    facility=chempion, schedule_type='instructor',
                    weekday=5, time_start='12:00', time_end='18:00',
                ),
                FacilityWorkingSchedule(
                    facility=chempion, schedule_type='break',
                    weekday=None, time_start='11:30', time_end='13:00',
                    note='Перерыв на обед',
                ),
            ])

        parent_sections = [
            ('equipment', 'Что взять на тренировку', (
                '<ul><li>Спортивная форма и обувь</li>'
                '<li>Бутылка воды</li><li>Полотенце (для бассейна)</li>'
                '<li>Шапочка для плавания</li><li>Сменная обувь</li></ul>'
            )),
            ('medical', 'Медицинские справки', (
                '<p>Для посещения плавательного бассейна детям до 12 лет включительно '
                'необходима медицинская справка. С 12 лет справка не требуется.</p>'
                '<p>Для занятий в тренажёрном зале: до 16 лет — только с инструктором; '
                'с 16 до 17 лет — с письменного согласия родителей; с 17 лет — самостоятельно.</p>'
            )),
            ('rules', 'Правила посещения', (
                '<p>Соблюдайте расписание занятий и сеансов. Приходите за 10–15 минут до начала. '
                'Имейте при себе документ, удостоверяющий личность (для взрослых).</p>'
            )),
            ('safety', 'Техника безопасности', (
                '<p>Следуйте указаниям тренера и администрации. '
                'Не допускайте самостоятельных занятий без разрешения в зонах повышенной опасности.</p>'
            )),
            ('pool_rules', 'Правила бассейна', (
                '<p>Обязательно принять душ перед входом в бассейн. '
                'Использовать шапочку для плавания. Соблюдать дистанцию и правила дорожек.</p>'
            )),
            ('gto', 'ГТО', (
                '<p>Информация о сдаче норм ГТО уточняется у тренеров и администрации спортивных школ.</p>'
            )),
            ('faq', 'Частые вопросы', (
                '<p><strong>Когда обновится расписание?</strong> '
                'С 1 сентября будет опубликовано новое расписание на учебный год.</p>'
                '<p><strong>Как арендовать зал?</strong> '
                'Позвоните по телефону объекта и скачайте прейскурант на сайте.</p>'
            )),
        ]
        for section, title, content in parent_sections:
            ParentInfo.objects.update_or_create(
                section=section,
                defaults={'title': title, 'content': content},
            )

        if not News.objects.exists():
            News.objects.create(
                title='Расписание на июль 2026 опубликовано',
                slug='raspisanie-iyul-2026',
                body=(
                    'На сайте опубликовано расписание занятий и сеансов бассейна на июль 2026 года. '
                    'С августа расписание будет обновлено в связи с началом учебного процесса.'
                ),
                category='event',
                published_at=timezone.now(),
            )
            News.objects.create(
                title='Набор в секцию плавания',
                slug='nabor-plavanie',
                body=(
                    'Спортивная школа «Кама» проводит набор детей от 7 до 18 лет '
                    'в секцию плавания. Обращайтесь по телефону или приходите в СК «Единая Россия».'
                ),
                category='recruitment',
                published_at=timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS('Начальные данные успешно загружены!'))
