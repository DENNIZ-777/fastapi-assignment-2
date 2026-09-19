import http
import logging

logger = logging.getLogger('uvicorn.error')

class CustomException(Exception):
    def __init__(
        self,
        status_code: int = 500,
        error_code: str = "ERROR_000",
        error_message: str = "Unexpected error occurred"
    ):
        if not isinstance(status_code, int) or status_code not in http.HTTPStatus.__members__.values():
            logger.critical(f"Invalid status_code {status_code} provided to CustomException, defaulting to 500")
            self.status_code = 500
        else:
            self.status_code = status_code
            
        if not isinstance(error_code, str):
            logger.critical(f"Invalid error_code {str(error_code)} provided to CustomException,"
                            " defaulting to 'ERROR_000'")
            self.error_code = "ERR_000"
        else:
            self.error_code = error_code
        
        if not isinstance(error_message, str):
            self.error_message = http.HTTPStatus(self.status_code).description
            logger.critical(f"Invalid error_message {str(error_message)} provided to CustomException,"
                            f" defaulting to '{self.error_message}'")
        else:
            self.error_message = error_message