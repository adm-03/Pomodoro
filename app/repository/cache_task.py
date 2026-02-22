from redis import asyncio as Redis
import json
from app.schema.task import Task

class CacheTask:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[Task]:
        task_json = await self.redis.lrange("tasks", 0, -1)
        return [Task.model_validate_json(t) for t in task_json]

    
    async def set_task(self, tasks: list[Task]):
        tasks_json = [task.model_dump_json() for task in tasks]
        await self.redis.lpush("tasks", *tasks_json)