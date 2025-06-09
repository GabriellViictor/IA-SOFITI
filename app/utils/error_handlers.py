from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST
import logging
import json

def setup_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logging.error(f"HTTPException: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logging.error(f"Validation error: {exc.errors()}")
        errors = exc.errors()
        custom_errors = [
            {
                "campo": ".".join(str(loc) for loc in err["loc"][1:]),
                "mensagem": err["msg"]
            }
            for err in errors
        ]
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"erro_validacao": custom_errors},
        )
    

    @app.middleware("http")
    async def catch_json_decode_errors(request: Request, call_next):
        try:
            return await call_next(request)
        except json.JSONDecodeError as exc:
            logging.error(f"JSON decode error: {str(exc)}")
            return JSONResponse(
                status_code=HTTP_400_BAD_REQUEST,
                content={
                    "erro_validacao": [
                        {
                            "campo": "body",
                            "mensagem": "Erro de formatação no JSON: JSON inválido."
                        }
                    ]
                },
            )
        except Exception as exc:
            logging.error(f"Unhandled error in middleware: {str(exc)}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Erro interno do servidor."},
            )
        