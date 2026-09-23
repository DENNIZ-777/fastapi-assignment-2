class CustomException(Exception):
    def __init__(
        self,
        status_code: int = 500,
        error_code: str = "ERR_000",
        error_message: str = "Unexpected error occurred"
    ):
        super().__init__(error_message)
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message


class MissingValueException(CustomException):
    def __init__(self) -> None:
        super().__init__(422, "ERR_001", "MISSING VALUE")


class InvalidPasswordException(CustomException):
    def __init__(self) -> None:
        super().__init__(422, "ERR_002", "INVALID PASSWORD")


class InvalidPhoneNumberException(CustomException):
    def __init__(self) -> None:
        super().__init__(422, "ERR_003", "INVALID PHONE NUMBER")


class BioTooLongException(CustomException):
    def __init__(self) -> None:
        super().__init__(422, "ERR_004", "BIO TOO LONG")


class EmailAlreadyExistsException(CustomException):
    def __init__(self) -> None:
        super().__init__(409, "ERR_005", "EMAIL ALREADY EXISTS")


class InvalidSessionException(CustomException):
    def __init__(self) -> None:
        super().__init__(401, "ERR_006", "INVALID SESSION")


class BadAuthorizationHeaderException(CustomException):
    def __init__(self) -> None:
        super().__init__(400, "ERR_007", "BAD AUTHORIZATION HEADER")


class InvalidTokenException(CustomException):
    def __init__(self) -> None:
        super().__init__(401, "ERR_008", "INVALID TOKEN")


class UnauthenticatedException(CustomException):
    def __init__(self) -> None:
        super().__init__(401, "ERR_009", "UNAUTHENTICATED")


class InvalidAccountException(CustomException):
    def __init__(self) -> None:
        super().__init__(401, "ERR_010", "INVALID ACCOUNT")
