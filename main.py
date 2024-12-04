
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from app.api.endpoints import auth, money_management
from app.core.exceptions import NotFoundException, BadRequestException, UnauthorizedException
from app.models.api import APIResponse

routes = FastAPI()

routes.include_router(auth.router, tags=["auth"])
routes.include_router(money_management.router, prefix="/money", tags=["money"])

# Mount the static files directory
routes.mount("/static", StaticFiles(directory="static"), name="static")

@routes.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(status="error", message=str(exc.detail), data=None).dict()
    )

@routes.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(status="error", message=str(exc.detail), data=None).dict()
    )

@routes.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(status="error", message=str(exc.detail), data=None).dict(),
        headers=exc.headers
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(routes, host="0.0.0.0", port=8000)

