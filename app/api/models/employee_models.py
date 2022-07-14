from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate
from typing import Optional, List
from http import HTTPStatus


@dataclass
class EmployeeResponse:
    id: str
    name: str
    last_name: str
    nickname: str
    main_technology: str
    programmer_level: str
    status: str
    project_end_date: Optional[str] = None
    cv: Optional[str] = None
    additional_data: Optional[str] = None


@dataclass
class GetEmployeesResponse:
    employees: List[EmployeeResponse]


@dataclass_validate
@dataclass
class EmployeeFilterRequest:
    main_technology: str
    programmer_level: str
    status: Optional[str] = None
    date: Optional[int] = None


@dataclass_validate
@dataclass
class EmployeeSearchRequest:
    data: str


@dataclass_validate
@dataclass
class EmployeeAddRequest:
    name: str
    last_name: str
    main_technology: str
    programmer_level: str
    status: str
    project_end_date: Optional[str] = None
    cv: Optional[str] = None
    additional_data: Optional[str] = None


@dataclass_validate
@dataclass
class EmployeeUpdateRequest:
    name: Optional[str] = None
    last_name: Optional[str] = None
    main_technology: Optional[str] = None
    programmer_level: Optional[str] = None
    status: Optional[str] = None
    project_end_date: Optional[str] = None
    cv: Optional[str] = None
    additional_data: Optional[str] = None


class ResponseModel:

    @staticmethod
    def response_ok(message: str = 'OK', code: HTTPStatus = HTTPStatus.OK) -> dict:
        """Notifies the status code (OK) and message"""

        return {'code': code, 'message': message}

    @staticmethod
    def response_created(message: str = 'OK', code: HTTPStatus = HTTPStatus.CREATED) -> dict:
        """Notifies the status code (CREATED) and message"""

        return {'code': code, 'message': message}
