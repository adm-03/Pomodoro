from fastapi import FastAPI, APIRouter, status, Depends
from dependencies import get_task_repository, get_cache_repository, get_task_service
from repository import TaskRepository, CacheTask
from fixtures import tasks as fixtures_tasks
from schema.task import TaskCreate, Task
from service import TaskService
from typing import Annotated

router = APIRouter(prefix="/task", tags=["task"])



@router.get("/all", response_model=list[Task])
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return task_service.get_tasks()
    

@router.post("/", response_model=Task) 
async def create_task(task: TaskCreate, task_repository: Annotated[TaskRepository, Depends(get_task_repository)]):
    new_task = task_repository.create_task(task)
    
    return new_task


@router.patch("/{task_id}", response_model=Task)
async def patch_task(task_id: int, name: str, task_repository: Annotated[TaskRepository, Depends(get_task_repository)]):
    return task_repository.update_task_name(task_id, name)



@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, task_repository: Annotated[TaskRepository, Depends(get_task_repository)] ):
    task_repository.delete_task(task_id)