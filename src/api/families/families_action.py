from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import constants
from core.exceptions import UserCannotLeaveFamily
from db.dals.families import AsyncFamilyDAL
from db.dals.users import AsyncUserDAL
from schemas.families import FamilyShow
from schemas.users import UserCreate, UserFamilyPermissionModel
from db.models.user import User
from services.families.data import FamilyDataService
from services.families.services import AddUserToFamilyService, FamilyCreatorService, LogoutUserFromFamilyService


from logging import getLogger
logger = getLogger(__name__)

user_router = APIRouter()


async def _create_family(
    user: User, body: UserCreate, async_session: AsyncSession
) -> FamilyShow:

    try:
        async with async_session.begin():
            family = await FamilyCreatorService(
                name=body.name, user=user, db_session=async_session
            )()
            return FamilyShow(name=family.name)
    except ValueError as e:
        return JSONResponse(
            status_code=400, content={"detail": "The user is already a family member"}
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})

async def _get_family(user: User, async_session: AsyncSession) -> FamilyShow | HTTPException:
    async with async_session.begin():
        data = await FamilyDataService(async_session).get_family_with_users(
            user.family_id
        )
        if data is None:
            raise HTTPException(status_code=404, detail=f"Family not found")

        return data

async def _add_user_to_family(family_id, user_id: User, async_session: AsyncSession) -> None:
    async with async_session.begin():
        family = await AsyncFamilyDAL(async_session).get_by_id(family_id)
        user = await AsyncUserDAL(async_session).get_by_id(user_id)

        permission = UserFamilyPermissionModel(**constants.default_user_permissions)

        await AddUserToFamilyService(
            family=family,
            user=user,
            permissions=permission,
            is_family_admin=False,
            db_session=async_session
        )()
        return JSONResponse(
            content={"message": "OK"},
            status_code=200,
        )


async def _logout_user_from_family(user: User, async_session: AsyncSession) -> JSONResponse:
    async with async_session.begin():
        try:
            await LogoutUserFromFamilyService(user=user, db_session=async_session)()

        except UserCannotLeaveFamily:
            return JSONResponse(
                content={"message": "You cannot leave a family while you are its administrator."},
                status_code=400,
            )
        
        return JSONResponse(
            content={"message": "OK"},
            status_code=200,
        )