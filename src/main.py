from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from tests.util import get_all_src_py_files_hash
from src.api import api_router
from src.common.custom_exception import (
    BioTooLongException,
    CustomException,
    InvalidPasswordException,
    InvalidPhoneNumberException,
    MissingValueException,
)

app = FastAPI()

app.include_router(api_router)

@app.exception_handler(CustomException)
def handle_custom_exception(_: Request, exc: CustomException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": exc.error_code, "error_msg": exc.error_message},
    )


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    validation_error = exc.errors()[0]
    exception_by_type = {
        "missing": MissingValueException,
        "invalid_password": InvalidPasswordException,
        "invalid_phone_number": InvalidPhoneNumberException,
        "bio_too_long": BioTooLongException,
    }
    exception_type = exception_by_type.get(validation_error["type"])
    if exception_type is None:
        return await request_validation_exception_handler(request, exc)

    error = exception_type()
    return JSONResponse(
        status_code=error.status_code,
        content={"error_code": error.error_code, "error_msg": error.error_message},
    )

@app.get("/health")
def health_check():
    # 서버 정상 배포 여부를 확인하기 위한 엔드포인트입니다.
    # 본 코드는 수정하지 말아주세요!
    hash = get_all_src_py_files_hash()
    return {
        "status": "ok",
        "hash": hash
    }
