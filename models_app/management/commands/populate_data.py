import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from models_app.models import Project, Task, Subtask, UserProject, TaskUser, Dashboard, Timer, User


class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **kwargs):
        # Получение списка id пользователей
        user_ids = list(User.objects.all().values_list("id", flat=True))
        if not user_ids:
            self.stdout.write(self.style.ERROR('Нет доступных пользователей в базе данных'))
            return

        # Данные для проектов
        project_data = [
            {'name': 'Разработка веб-сайта компании', 'image': 'data/даша.jpg'},
            {'name': 'Мобильное приложение для заказа еды', 'image': 'data/даша.jpg'},
            {'name': 'Система управления проектами', 'image': 'data/даша.jpg'},
            {'name': 'Онлайн-магазин электроники', 'image': 'data/даша.jpg'},
            {'name': 'Платформа для онлайн-обучения', 'image': 'data/даша.jpg'}
        ]

        # Создание проектов
        projects = []
        for data in project_data:
            project = Project.objects.create(
                name=data['name'],
                image=data['image']
            )
            projects.append(project)

        self.stdout.write(self.style.SUCCESS(f'Создано {len(projects)} проектов'))

        # Данные для статусов
        status_data = [
            'К выполнению', 'В процессе', 'Завершено', 'На проверке', 'Отложено', 'В доработке', 'На утверждении'
        ]

        # Создание статусов задач (Dashboards)
        dashboards = []
        for project in projects:
            for i, status in enumerate(status_data):
                dashboard = Dashboard.objects.create(
                    status=status,
                    position=i + 1,
                    project=project,
                    color=f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'
                )
                dashboards.append(dashboard)

        self.stdout.write(self.style.SUCCESS(f'Создано {len(dashboards)} статусов'))

        # Данные для задач
        task_data = [
            {'title': 'Разработка главной страницы', 'description': 'Создать и оформить главную страницу сайта'},
            {'title': 'Настройка базы данных', 'description': 'Настроить и оптимизировать базу данных'},
            {'title': 'Создание пользовательского интерфейса',
             'description': 'Разработать UI для мобильного приложения'},
            {'title': 'Интеграция платежной системы', 'description': 'Подключить и настроить систему онлайн-платежей'},
            {'title': 'Написание тестов', 'description': 'Создать автоматические тесты для основных функций'},
            {'title': 'SEO оптимизация', 'description': 'Оптимизировать сайт для поисковых систем'},
            {'title': 'Обучение сотрудников', 'description': 'Провести тренинги для сотрудников по новому ПО'},
            {'title': 'Создание маркетинговой кампании',
             'description': 'Разработать стратегию и материалы для продвижения'},
            {'title': 'Техническая поддержка', 'description': 'Настроить и обеспечить техподдержку для пользователей'},
            {'title': 'Анализ данных', 'description': 'Собрать и проанализировать данные о пользователях'},
            {'title': 'Обновление дизайна', 'description': 'Обновить дизайн сайта'},
            {'title': 'Разработка мобильной версии', 'description': 'Разработать мобильную версию сайта'},
            {'title': 'Интеграция с CRM', 'description': 'Интегрировать систему с CRM'},
            {'title': 'Настройка уведомлений', 'description': 'Настроить уведомления для пользователей'},
            {'title': 'Поддержка пользователей', 'description': 'Обеспечить поддержку пользователей'},
            {'title': 'Планирование спринта', 'description': 'Планировать задачи на спринт'},
            {'title': 'Проработка технического задания', 'description': 'Проработать техническое задание'},
            {'title': 'Ведение документации', 'description': 'Вести документацию по проекту'},
            {'title': 'Оптимизация кода', 'description': 'Оптимизировать код для повышения производительности'}
        ]

        # Создание задач
        tasks = []
        for dashboard in dashboards:
            num_tasks = random.randint(2, 5)
            selected_task_indices = random.sample(range(len(task_data)), num_tasks)
            for task_index in selected_task_indices:
                task_info = task_data[task_index]
                task = Task.objects.create(
                    title=task_info['title'],
                    description=task_info['description'],
                    time_per_task=random.randint(10, 50),
                    status=dashboard,
                    project=dashboard.project,
                    author_id=random.choice(user_ids)
                )
                tasks.append(task)

        self.stdout.write(self.style.SUCCESS(f'Создано {len(tasks)} задач'))

        # Данные для подзадач
        subtask_titles = [
            'Дизайн макета', 'Верстка', 'Тестирование', 'Создание схемы БД', 'Написание SQL запросов',
            'Оптимизация запросов', 'Разработка UI макета', 'Реализация интерфейса', 'Интеграция API',
            'Тестирование платежей', 'Обучение использования', 'Создание unit-тестов', 'Создание интеграционных тестов',
            'Тестирование тестов', 'Анализ ключевых слов', 'Оптимизация контента', 'Проверка индексации',
            'Подготовка материалов', 'Проведение тренинга', 'Анализ эффективности'
        ]

        subtask_descriptions = [
            'Создать дизайн макета страницы', 'Написать HTML/CSS код для страницы', 'Провести тестирование верстки',
            'Разработать схему базы данных', 'Написать необходимые SQL запросы', 'Оптимизировать SQL запросы',
            'Создать макет пользовательского интерфейса', 'Написать код для интерфейса',
            'Подключить API платежной системы',
            'Провести тестирование платежной системы', 'Создать документацию по использованию системы',
            'Написать unit-тесты для основных функций', 'Написать интеграционные тесты', 'Провести тестирование тестов',
            'Провести анализ ключевых слов для SEO', 'Оптимизировать контент для SEO', 'Проверить индексацию сайта',
            'Создать материалы для тренинга', 'Провести тренинг для сотрудников', 'Анализировать эффективность обучения'
        ]

        # Создание подзадач
        subtasks = []
        for task in tasks:
            num_subtasks = random.randint(2, 4)
            selected_subtask_indices = random.sample(range(len(subtask_titles)), num_subtasks)
            for subtask_index in selected_subtask_indices:
                subtask = Subtask.objects.create(
                    title=subtask_titles[subtask_index],
                    description=subtask_descriptions[subtask_index],
                    is_done=random.choice([True, False]),
                    task=task
                )
                subtasks.append(subtask)

        self.stdout.write(self.style.SUCCESS(f'Создано {len(subtasks)} подзадач'))

        # Создание UserProject
        user_projects = []
        for user_id in user_ids:
            for project in projects:
                user_project = UserProject.objects.create(
                    user_id=user_id,
                    project=project
                )
                user_projects.append(user_project)

        self.stdout.write(self.style.SUCCESS(f'Создано {len(user_projects)} записей UserProject'))

        # Создание TaskUser
        task_users = []
        for task in tasks:
            assigned_user_ids = random.sample(user_ids, random.randint(1, len(user_ids)))
            for user_id in assigned_user_ids:
                task_user = TaskUser.objects.create(
                    user_id=user_id,
                    task=task
                )
                task_users.append(task_user)

        self.stdout.write(self.style.SUCCESS(f'Создано {len(task_users)} записей TaskUser'))

        # Создание таймеров
        timers = []
        for task_user in task_users:
            num_timers = random.randint(1, 3)
            for _ in range(num_timers):
                start_time = timezone.now() - timezone.timedelta(hours=random.randint(1, 10))
                end_time = start_time + timezone.timedelta(hours=random.randint(1, 5))
                timer = Timer.objects.create(
                    start_time=start_time,
                    end_time=end_time,
                    result_time=end_time - start_time,
                    task_user=task_user
                )
                timers.append(timer)

        self.stdout.write(self.style.SUCCESS(f'Создано {len(timers)} таймеров'))
