import traceback

from typing import Callable
from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from uvicorn.protocols.utils import ClientDisconnected

from app.core.middlewares import send_log_to_discord
from app.core.config import settings


class ExceptionLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
    
        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as exc:
                if isinstance(exc, HTTPException):
                    return JSONResponse(status_code=exc.status_code, content=exc.detail)
    
                try:
                    body = await request.json()
                except Exception:
                    try:
                        body = await request.form()
                    except Exception:
                        body = "Unable to parse body"
            
                payload = {
                    "url": str(request.url),
                    "method": str(request.method),
                    "client": str(request.client),
                    "headers": str(request.headers),
                    "query_params": str(request.query_params),
                    "body": body,
                }

                if exc and not isinstance(exc, (ClientDisconnected)):
                    await send_log_to_discord(str(traceback.format_exc()), payload=payload)
                    if settings.IS_DEV:
                        print(str(traceback.format_exc()))
                return JSONResponse(status_code=500, content={"message": "An internal server error occurred"})
        
        return custom_route_handler