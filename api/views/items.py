from config import Config
from db import get_session
from starlette.requests import Request
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.repositories import items_repository
from api.utils import check_content_type_and_get_data


router = APIRouter(
    prefix=f"{Config.API_ROUTER_PREFIX}/items",
    tags=["Items"],
)



@router.post("/create",) 
async def incoming_ping(request: Request, session: AsyncSession = Depends(get_session)):
    validated_data = await check_content_type_and_get_data(request)
    validated_data['data']['ip_address'] = request.client.host
    response = await items_repository.process_data(session, validated_data)
    return response