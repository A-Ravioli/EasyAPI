from celery import Celery
from celery.result import AsyncResult


class TaskQueueService:
    def __init__(self, broker_url, backend_url=None):
        self.app = Celery("tasks", broker=broker_url, backend=backend_url)

    def add_task(self, func, *args, **kwargs):
        """
        Add a task to the queue with the given arguments.
        """
        return self.app.send_task(func, args=args, kwargs=kwargs)

    def get_result(self, task_id):
        """
        Get the result of a task by its ID.
        """
        result = AsyncResult(task_id, app=self.app)
        return result.result, result.status

    def retry_task(self, task_id, countdown=60):
        """
        Retry a failed task after a given countdown.
        """
        result = AsyncResult(task_id, app=self.app)
        if not result.successful():
            result.retry(countdown=countdown)
