from fastapi import APIRouter

from app.core.exception_handler import ExceptionLoggingRoute

router = APIRouter(route_class=ExceptionLoggingRoute)


@router.get("/")
async def common():
    return {"message": "First api endpoint."}