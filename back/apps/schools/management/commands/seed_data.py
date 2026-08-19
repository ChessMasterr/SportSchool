from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.content.models import GalleryAlbum, GalleryImage, Document, News, ParentInfo, SiteSettings
from apps.schedules.models import FacilityWorkingSchedule, PoolSession, ScheduleEntry, SchedulePeriod
from apps.schools.models import Coach, Facility, PriceItem, School, SportDirection


class Command(BaseCommand):
    help = 'Загрузка начальных данных для сайта спортивных школ'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка начальных данных...')

        settings = SiteSettings.load()
        settings.site_title = 'Спортивные школы Елабуги'
        settings.hero_title = 'Секции спортивных школ Елабуги'
        settings.hero_subtitle = (
            'Выберите секцию — узнайте, где проходят занятия, '
            'и посмотрите актуальное расписание.'
        )
        settings.email = 'olymp.elabuga@mail.ru'
        settings.vk_url = 'https://vk.com/public217310680'
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

        olymp, _ = School.objects.update_or_create(
            slug='olymp',
            defaults={
                'name': 'МБУ ДО «СШ «Олимп» ЕМР РТ',
                'short_description': (
                    'Муниципальное бюджетное учреждение дополнительного образования '
                    '«Спортивная школа «Олимп» Елабужского муниципального района.'
                ),
                'full_description': (
                    'Полное название: Муниципальное бюджетное учреждение дополнительного '
                    'образования «Спортивная школа «Олимп» Елабужского муниципального района '
                    'Республики Татарстан. Директор — Галимов Ильнар Глусович. '
                    'Есть возможность арендовать футбольный манеж, теннисные корты, ледовую арену.'
                ),
                'order': 2,
                'is_active': True,
            },
        )

        School.objects.update_or_create(
            slug='yunost',
            defaults={
                'name': 'СШ «Юность»',
                'short_description': 'Спортивная школа «Юность»',
                'order': 3,
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
                'slug': 'edinaya-rossiya',
                'school': olymp,
                'name': 'СК «Единая Россия»',
                'facility_type': 'game_hall',
                'address': 'ул. Тази Гиззата, 31, Елабуга, Респ. Татарстан, 423602',
                'phone': '8 (855) 573-47-17',
                'working_hours': '08:00 — 21:00',
                'description': 'Спортивный комплекс: игровые залы, теннис, танцевальный спорт и другие секции.',
                'has_hall_rental': True,
                'hall_rental_note': 'Возможна аренда. Уточняйте по телефону объекта.',
                'order': 2,
            },
            {
                'slug': 'central-stadium',
                'school': olymp,
                'name': 'Центральный стадион',
                'facility_type': 'other',
                'address': 'ул. Василия Горшунова, 1, Елабуга, Респ. Татарстан, 423602',
                'phone': '8 (855) 573-60-24',
                'working_hours': '08:00 — 21:00',
                'order': 3,
            },
            {
                'slug': 'atletics-manege',
                'school': olymp,
                'name': 'Легкоатлетический манеж',
                'facility_type': 'other',
                'address': 'ул. Тази Гиззата, 27а, Елабуга, Респ. Татарстан, 423602',
                'phone': '8 (855) 573-43-32',
                'working_hours': '08:00 — 21:00',
                'order': 4,
            },
            {
                'slug': 'ice-palace',
                'school': olymp,
                'name': 'Ледовый дворец',
                'facility_type': 'other',
                'address': 'ул. Тази Гиззата, 27, Елабуга, Респ. Татарстан, 423602',
                'phone': '8 (855) 573-21-00',
                'working_hours': '08:00 — 21:00',
                'has_hall_rental': True,
                'hall_rental_note': 'Возможна аренда ледовой арены. Уточняйте по телефону.',
                'order': 5,
            },
            {
                'slug': 'august-manege',
                'school': olymp,
                'name': 'Футбольный манеж «Август»',
                'facility_type': 'game_hall',
                'address': 'ул. Тугарова, 85, Елабуга, Респ. Татарстан, 423602',
                'phone': '8 (855) 575-71-03',
                'working_hours': '08:00 — 21:00',
                'has_hall_rental': True,
                'hall_rental_note': 'Возможна аренда футбольного манежа. Уточняйте по телефону.',
                'order': 6,
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
                'order': 7,
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
                'order': 8,
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
                'order': 9,
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
                'order': 10,
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

        olymp_directions = [
            {
                'slug': 'futbol',
                'name': 'Футбол',
                'facility': 'august-manege',
                'coaches': [
                    'Ахметов Н.М.', 'Валикаев А.Р.', 'Гильфанов Д.Р.',
                    'Мальчиков С.А.', 'Тухватуллин А.С.',
                ],
            },
            {
                'slug': 'voleybol',
                'name': 'Волейбол',
                'facility': 'edinaya-rossiya',
                'coaches': ['Турьева А.С.', 'Надеждин Д.А.'],
            },
            {
                'slug': 'tennis',
                'name': 'Теннис',
                'facility': 'edinaya-rossiya',
                'coaches': ['Усманова А.Р.'],
            },
            {
                'slug': 'tancevalnyj-sport',
                'name': 'Танцевальный спорт',
                'facility': 'edinaya-rossiya',
                'coaches': ['Биккинин Р.Р.'],
            },
            {
                'slug': 'badminton',
                'name': 'Бадминтон',
                'facility': 'edinaya-rossiya',
                'coaches': ['Корочкин Н.Е.', 'Тагирова Р.Р.'],
            },
            {
                'slug': 'hudozhestvennaya-gimnastika',
                'name': 'Художественная гимнастика',
                'facility': 'edinaya-rossiya',
                'coaches': ['Раджабова Н.А.', 'Раджабова А.Ш.', 'Чернышова С.Ш.'],
            },
            {
                'slug': 'legkaya-atletika',
                'name': 'Лёгкая атлетика',
                'facility': 'atletics-manege',
                'coaches': ['Шаманаев Б.Н.', 'Рожин М.С.'],
            },
            {
                'slug': 'lyzhnye-gonki',
                'name': 'Лыжные гонки',
                'facility': 'central-stadium',
                'coaches': ['Трущин С.А.', 'Печников К.Д.'],
            },
            {
                'slug': 'figurnoe-katanie',
                'name': 'Фигурное катание на коньках',
                'facility': 'ice-palace',
                'coaches': ['Галимрахманова А.Н.', 'Ахмедова Л.Р.'],
            },
            {
                'slug': 'hokkej',
                'name': 'Хоккей',
                'facility': 'ice-palace',
                'coaches': [
                    'Жужгов Р.Е.', 'Галимов И.И.', 'Герасимов А.А.', 'Галимов И.С.',
                ],
            },
        ]

        olymp_dirs = {}
        for i, item in enumerate(olymp_directions):
            direction, _ = SportDirection.objects.update_or_create(
                school=olymp,
                slug=item['slug'],
                defaults={
                    'facility': facilities[item['facility']],
                    'name': item['name'],
                    'description': (
                        f'Секция «{item["name"]}» СШ «Олимп». '
                        f'Занятия проходят: {facilities[item["facility"]].name}.'
                    ),
                    'order': i + 2,
                },
            )
            olymp_dirs[item['slug']] = direction

            for j, coach_name in enumerate(item['coaches']):
                coach, _ = Coach.objects.update_or_create(
                    school=olymp,
                    full_name=coach_name,
                    defaults={
                        'facility': facilities[item['facility']],
                        'order': j + 1,
                        'is_active': True,
                    },
                )
                coach.sport_directions.add(direction)

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
                    'order': i + 20,
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

        # Прейскурант как "документ" (чтобы скачивание/вывод был единообразным)
        price_doc = Document.objects.filter(school=kama, doc_type='price_list').first()
        price_content = '<ul>' + ''.join(
            [
                f'<li>{name}: <strong>{price}</strong></li>'
                for (name, price) in prices
            ]
        ) + '</ul>'
        if not price_doc:
            Document.objects.create(
                school=kama,
                doc_type='price_list',
                title=f'Прейскурант СШ «{kama.name}»',
                content=price_content,
                order=1,
                is_published=True,
            )
        else:
            price_doc.title = f'Прейскурант СШ «{kama.name}»'
            price_doc.content = price_content
            price_doc.order = 1
            price_doc.is_published = True
            price_doc.save()

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

        gallery_albums = [
            {
                'slug': 'trenirovki-plavanie',
                'category': 'training',
                'title': 'Тренировки секции плавания',
                'description': 'Тренировочный процесс в бассейне СШ «Кама».',
                'event_date': '2026-07-10',
                'school': kama,
                'order': 1,
            },
            {
                'slug': 'trenirovki-futbol',
                'category': 'training',
                'title': 'Тренировки секции футбола',
                'description': 'Занятия в футбольном манеже «Август».',
                'event_date': '2026-07-12',
                'school': olymp,
                'order': 2,
            },
            {
                'slug': 'kubok-elabugi-futbol-2026',
                'category': 'competition',
                'title': 'Кубок Елабуги по футболу',
                'description': 'Фотографии с городского турнира.',
                'event_date': '2026-06-15',
                'school': olymp,
                'order': 1,
            },
            {
                'slug': 'pervenstvo-plavanie-2026',
                'category': 'competition',
                'title': 'Первенство по плаванию',
                'description': 'Соревнования воспитанников СШ «Кама».',
                'event_date': '2026-05-20',
                'school': kama,
                'order': 2,
            },
            {
                'slug': 'nagrazhdenie-pobeditelej-2026',
                'category': 'awards',
                'title': 'Награждение победителей сезона',
                'description': 'Церемония награждения спортсменов по итогам сезона.',
                'event_date': '2026-06-01',
                'school': olymp,
                'order': 1,
            },
            {
                'slug': 'video-sorevnovaniya',
                'category': 'video',
                'title': 'Видео с соревнований',
                'description': 'Видеозаписи турниров и первенств.',
                'event_date': '2026-06-15',
                'school': None,
                'order': 1,
            },
        ]
        for data in gallery_albums:
            GalleryAlbum.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'category': data['category'],
                    'description': data['description'],
                    'event_date': data['event_date'],
                    'school': data['school'],
                    'order': data['order'],
                    'is_published': True,
                },
            )

        for image in GalleryImage.objects.filter(album__isnull=True):
            category = image.category if image.category in dict(GalleryAlbum.CATEGORY_CHOICES) else 'training'
            fallback, _ = GalleryAlbum.objects.get_or_create(
                slug=f'prochee-{category}',
                defaults={
                    'title': f'Прочие материалы: {dict(GalleryAlbum.CATEGORY_CHOICES)[category]}',
                    'category': category,
                    'is_published': True,
                    'order': 99,
                },
            )
            image.album = fallback
            image.save()

        self.stdout.write(self.style.SUCCESS('Начальные данные успешно загружены!'))
