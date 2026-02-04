from dataclasses import dataclass
from models import Tasks
from repository import TaskRepository, CacheTask
from schema import Task, TaskCreate
from exception import TaskNotFound
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
    
    def create_task(self, body: TaskCreate, user_id: int):
        task_id = self.task_repository.create_task(body, user_id)
        task = self.task_repository.get_task(task_id)
        return task
    
    def update_task_name(self, task_id: int, name: str, user_id: int) -> Tasks:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound 
        return self.task_repository.update_task_name(task_id=task_id, name=name)
    
    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound 
        self.task_repository.delete_task(task_id=task_id)
        