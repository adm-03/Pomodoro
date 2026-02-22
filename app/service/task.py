from dataclasses import dataclass
from app.models import Tasks
from app.repository import TaskRepository, CacheTask
from app.schema import Task, TaskCreate
from app.exception import TaskNotFound
@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    async def get_tasks(self) -> list[Task]:
        if cache_tasks := await self.task_cache.get_tasks():
            return cache_tasks
        else:
            tasks = await self.task_repository.get_tasks()
            tasks_pydantic = [Task.model_validate(t) for t in tasks]
            await self.task_cache.set_task(tasks_pydantic)
        return tasks_pydantic
    
    async def create_task(self, body: TaskCreate, user_id: int):
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task(task_id)
        return task
    
    async def update_task_name(self, task_id: int, name: str, user_id: int) -> Task:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound 
        sql_task = await self.task_repository.update_task_name(task_id=task_id, name=name)
        return Task.model_validate(sql_task)
    
    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound 
        await self.task_repository.delete_task(task_id=task_id)
        