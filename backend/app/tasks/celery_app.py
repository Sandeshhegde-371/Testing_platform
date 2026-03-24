"""
app/tasks/celery_app.py

Celery application factory.

Configures the Celery instance with:
    - Redis as broker and result backend
    - Task serialisation (JSON)
    - Task routing (dedicated queues per domain)
    - Retry policies and timeouts
    - Periodic tasks (via celery.beat_schedule)

Usage:
    # In a task file:
    from app.tasks.celery_app import celery

    @celery.task(bind=True)
    def my_task(self, ...):
        ...
"""

from celery import Celery
# from app.core.config import settings


def create_celery() -> Celery:
    """
    Factory function that creates and configures the Celery application.

    Configuration:
        broker_url            : Redis queue for task distribution.
        result_backend        : Redis store for task results.
        task_serializer       : JSON (human readable, secure).
        task_routes           : Route tasks to domain-specific queues.
        task_soft_time_limit  : Graceful timeout before SoftTimeLimitExceeded.
        task_time_limit       : Hard kill timeout.
        beat_schedule         : Periodic task definitions.

    Returns:
        Celery: Configured Celery instance.
    """
    app = Celery("testai")

    # app.conf.broker_url = settings.CELERY_BROKER_URL
    # app.conf.result_backend = settings.CELERY_RESULT_BACKEND
    # app.conf.task_serializer = "json"
    # app.conf.result_serializer = "json"
    # app.conf.accept_content = ["json"]
    # app.conf.timezone = "UTC"
    # app.conf.task_soft_time_limit = 300
    # app.conf.task_time_limit = 360

    # Task routing (each domain gets its own Celery queue)
    # app.conf.task_routes = {
    #     "app.tasks.generation_tasks.*": {"queue": "generation"},
    #     "app.tasks.zephyr_tasks.*":     {"queue": "zephyr"},
    #     "app.tasks.execution_tasks.*":  {"queue": "execution"},
    # }

    # Auto-discover tasks in all task modules
    # app.autodiscover_tasks(["app.tasks.generation_tasks", "app.tasks.zephyr_tasks", "app.tasks.execution_tasks"])

    return app


celery = create_celery()
