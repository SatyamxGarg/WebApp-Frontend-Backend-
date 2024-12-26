from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from app.schemas import ResponseWrapper

class CustomExceptionHandler:
    @staticmethod
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """
        Custom handler for HTTP exceptions.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content=ResponseWrapper(
                status="ERROR",
                message=exc.detail,
                data=None,
                error={"detail": exc.detail}
            ).__dict__,
        )

    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Custom handler for validation errors.
        """
        return JSONResponse(
            status_code=422,
            content=ResponseWrapper(
                status="ERROR",
                message="Validation error occurred",
                data=None,
                error={"detail": exc.errors()}
            ).__dict__,
        )

    @staticmethod
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Custom handler for all other unhandled exceptions.
        """
        return JSONResponse(
            status_code=500,
            content=ResponseWrapper(
                status="ERROR",
                message="An unexpected error occurred",
                data=None,
                error={"detail": str(exc)}
            ).__dict__,
        )
