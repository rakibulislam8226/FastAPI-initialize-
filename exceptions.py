from typing import Optional

from fastapi import status as http_status


class CustomApiException(Exception):
    """
    Default custom API exception.
    """

    status_code = http_status.HTTP_400_BAD_REQUEST
    default_detail = "An API exception occurred."
    data = None

    def __init__(self,
                 message: Optional[str] = None,
                 status_code: Optional[int] = None,
                 data: Optional[dict] = None):
        """
        Initialization of exceptions class object.
        """
        self.message = message or self.default_detail
        self.status_code = status_code or self.status_code
        self.data = data
        super().__init__(message)

    def __repr__(self) -> str:
        columns = ", ".join(
            [f"{k}={repr(v)}" for k, v in self.__dict__.items() if not k.startswith("_")]
        )
        return f"<{self.__class__.__name__}({columns})>"


class CustomSqlAlchemyException(CustomApiException):
    """
    SqlAlchemy exceptions handling.
    e.g. db connection is invalidated or session improperly closed, see PBN-229.
    """
    status_code = http_status.HTTP_408_REQUEST_TIMEOUT
    default_detail = "ORM error happened."

    def __init__(self,
                 message: Optional[str] = None):
        """
        Initialization of exceptions class object.
        """
        super().__init__(message)
        self.message = self.default_detail
        if message:
            self.message = f"{self.message} {message}"
