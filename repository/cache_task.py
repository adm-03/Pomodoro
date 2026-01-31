from redis import Redis
import json
from schema.task import Task

class CacheTask:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[Task]:
        task_json = self.redis.lrange("tasks", 0, -1)
        return [Task.model_validate_json(t) for t in task_json]

    
    def set_task(self, tasks: list[Task]):
        tasks_json = [task.model_dump_json() for task in tasks]
        with self.redis as redis:
            redis.lpush("tasks", *tasks_json)