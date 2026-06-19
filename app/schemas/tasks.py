from pydantic import BaseModel, constr


class TaskCreate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1)


class TaskUpdate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1) | None = None
    done: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool
