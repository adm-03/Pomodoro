from dataclasses import dataclass
from repository import TaskRepository, CacheTask
from schema.task import Task

@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    def get_tasks(self) -> list[Task]:
        if cache_tasks := self.task_cache.get_tasks():
            return cache_tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_pydantic = [Task.model_validate(t) for t in tasks]
            self.task_cache.set_task(tasks_pydantic)
        return tasks_pydantic