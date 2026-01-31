from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

# 1. Базовая схема с логикой валидации
class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int 

    @model_validator(mode="after")
    def check_name_or_pomodoro_count_is_not_none(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("name or pomodoro count must be provided")
        return self

# 2. Схема для POST (наследует валидатор, ID нет)
class TaskCreate(TaskBase):
    pass

# 3. Схема для GET (наследует валидатор + добавляет ID)
class Task(TaskBase):
    id: int
    
