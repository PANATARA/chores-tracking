from uuid import UUID
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.auth_actions import get_current_user_from_token
from api.chores_logs.chores_logs_action import _confirm_chore_log, _create_chore_log
from db.models.user import User
from db.session import get_db
from schemas.chores_logs import ChoreLogConfirm, ChoreLogCreate


from logging import getLogger

logger = getLogger(__name__)

chores_logs_router = APIRouter()

# Create a new chorelog
@chores_logs_router.post("")
async def create_chore_log(
    body: ChoreLogCreate,
    current_user: User = Depends(get_current_user_from_token), 
    db: AsyncSession = Depends(get_db)
) -> Response:
    
    return await _create_chore_log(
        body=body,
        user=current_user,
        async_session=db
    )


@chores_logs_router.post(path="/confirm/{chorelog_id}")
async def confirm_chore_log(
    chorelog_id: UUID,
    body: ChoreLogConfirm,
    current_user: User = Depends(get_current_user_from_token), 
    db: AsyncSession = Depends(get_db)
) -> Response:
    
    return await _confirm_chore_log(
        chorelog_id,
        body=body,
        user=current_user,
        async_session=db
    )