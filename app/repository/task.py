from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Tasks, Categories
from app.schema.task import TaskCreate, Task


class TaskRepository:
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_tasks(self):
        task = (await self.db_session.execute(select(Tasks))).scalars().all()            
        return task
    
    
    async def get_task(self,  task_id: int) -> Tasks | None:
        task = (await self.db_session.execute(select(Tasks).where(Tasks.id == task_id))).scalar_one_or_none()
        return task
    
    async def create_task(self, task: TaskCreate, user_id: int) -> int:
        task_model = Tasks(
            name = task.name,
            pomodoro_count = task.pomodoro_count,
            category_id = task.category_id,
            user_id=user_id
        )
        self.db_session.add(task_model)
        await self.db_session.commit()
        return task_model.id

    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        task_id = await self.db_session.execute(query).scalar_one_or_none()
        await self.db_session.commit()
        return await self.get_task(task_id)

    async def delete_task(self, task_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id)
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        task: list[Tasks] = (await self.db_session.execute(query)).scalars().all()
        return task
        
    async def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query =  select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        task: Tasks = (await self.db_session.execute(query)).scalar_one_or_none()
        return task


