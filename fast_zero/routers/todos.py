from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import ToDo
from fast_zero.schemas import ToDoList, ToDoPublic, ToDoSchema, ToDoState, Message
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', response_model=ToDoPublic)
def create_to_do(
    todo: ToDoSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    db_todo = ToDo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=current_user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=ToDoList)
def list_todos(  # noqa
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    title: str | None = None,
    description: str | None = None,
    state: ToDoState | None = None,
    offset: int = None,
    limit: int = None,
):
    query = select(ToDo).where(ToDo.user_id == current_user.id)

    if title:
        query = query.where(ToDo.title.contains(title))

    if description:
        query = query.where(ToDo.description.contains(description))

    if state:
        query = query.where(ToDo.state == state)

    todos = session.scalars(query.limit(limit).offset(offset)).all()

    return {'todos': todos}

@router.delete('/', response_model=Message)
def delete_todo(
    todo_id: int = None,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    db_todo = session.scalar(select(ToDo).where(
        (ToDo.id == todo_id) | (ToDo.user_id == current_user.id)
        )
    )

    session.delete(db_todo)
    session.commit()

    return {'message': 'Task deleted successfully'}
