from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from dependencies import (
    get_task_repository,
    get_cache_repository,
    get_task_service,
    get_request_user_id,
)
from repository import TaskRepository, CacheTask
from fixtures import tasks as fixtures_tasks
from schema import TaskCreate, Task
from service import TaskService
from typing import Annotated
from exception import TaskNotFound

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[Task])
async def get_tasks(task_service: Annotated[TaskService, Depends(get_task_service)]):
    return await task_service.get_tasks()


@router.post("/", response_model=Task)
async def create_task(
    body: TaskCreate,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
):
    task = await task_service.create_task(body, user_id)
    return task


@router.patch("/{task_id}", response_model=Task)
async def patch_task(task_id: int,
                    name: str,
                    task_service: Annotated[TaskService, Depends(get_task_service)],
                    user_id: int = Depends(get_request_user_id)
):
    try:
        return await task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = e.detail
        )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = e.detail
        )