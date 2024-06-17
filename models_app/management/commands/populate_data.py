import random
import uuid
from django.core.management.base import BaseCommand
from models_app.models import User, Project, Task, Subtask, UserProject, TaskUser, Dashboard


class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **kwargs):
        # Создание проектов
        projects = []
        for i in range(1, 2):
            project = Project.objects.create(
                name=f'Project {i}',
                image=f'projects/project_{i}.jpg'
            )
            projects.append(project)

        self.stdout.write(self.style.SUCCESS(f'Created {len(projects)} projects'))

        # Создание статусов задач (Dashboards)
        dashboards = []
        statuses = ['To Do', 'In Progress', 'Done']
        for project in projects:
            for i, status in enumerate(statuses):
                dashboard = Dashboard.objects.create(
                    status=status,
                    position=i + 1,
                    project=project,
                    color=f'#{i * 2:02x}{i * 2:02x}{i * 2:02x}'
                )
                dashboards.append(dashboard)

        self.stdout.write(self.style.SUCCESS(f'Created {len(dashboards)} dashboards'))

        # Создание задач
        users_id = User.objects.all().values_list("id", flat=True)
        tasks = []
        for i in range(1, 11):
            task = Task.objects.create(
                title=f'Task {i}',
                description=f'This is the description for task {i}',
                time_per_task=i * 2,
                status=dashboards[i % len(dashboards)],
                project=projects[i % len(projects)],
                author_id=random.choice(users_id)
            )
            tasks.append(task)

        self.stdout.write(self.style.SUCCESS(f'Created {len(tasks)} tasks'))

        # Создание подзадач
        subtasks = []
        for i, task in enumerate(tasks):
            for j in range(1, 4):
                subtask = Subtask.objects.create(
                    title=f'Subtask {i * 3 + j}',
                    description=f'This is the description for subtask {i * 3 + j}',
                    is_done=(j % 2 == 0),
                    task=task
                )
                subtasks.append(subtask)

        self.stdout.write(self.style.SUCCESS(f'Created {len(subtasks)} subtasks'))

        # Создание UserProject
        user_projects = []
        for user_id in users_id:
            for project in projects:
                user_project = UserProject.objects.create(
                    user_id=user_id,
                    project=project
                )
                user_projects.append(user_project)

        self.stdout.write(self.style.SUCCESS(f'Created {len(user_projects)} user_projects'))

        # Создание TaskUser
        task_users = []
        for user_id in users_id:
            for task in tasks:
                task_user = TaskUser.objects.create(
                    user_id=user_id,
                    task=task
                )
                task_users.append(task_user)

        self.stdout.write(self.style.SUCCESS(f'Created {len(task_users)} task_users'))
