from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate
from typing import Optional
from http import HTTPStatus


@dataclass
class EmployeeResponse:
    id: str
    name: str
    last_name: str
    nickname: str
    main_technology: str
    status: str
    cv: Optional[str] = None
    additional_data: Optional[str] = None


@dataclass_validate
@dataclass
class EmployeeFilterRequest:
    main_technology: str


@dataclass_validate
@dataclass
class EmployeeSearchRequest:
    data: str
    # name: Optional[str] = None
    # last_name: Optional[str] = None
    # nickname: Optional[str] = None


@dataclass_validate
@dataclass
class EmployeeAddRequest:
    name: str
    last_name: str
    main_technology: str
    status: str
    cv: Optional[str] = None
    additional_data: Optional[str] = None


@dataclass_validate
@dataclass
class EmployeeUpdateRequest:
    name: Optional[str] = None
    last_name: Optional[str] = None
    main_technology: Optional[str] = None
    status: Optional[str] = None
    cv: Optional[str] = None
    additional_data: Optional[str] = None


class ResponseModel:

    @staticmethod
    def response_ok(message: str = 'OK', code: HTTPStatus = HTTPStatus.OK) -> dict:
        return {'code': code, 'message': message}


class APIError(Exception):
    def __init__(self, message, code: HTTPStatus = HTTPStatus.BAD_REQUEST):
        super().__init__()
        self.message = message
        self.code = code

    def to_dict(self) -> dict:
        return {'message': self.message, 'code': self.code}
