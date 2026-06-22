"""Custom exceptions."""


class ApiError(Exception):
    def __init__(self, status: int, message: str | None = None, data: dict | None = None):
        super().__init__(f"{status} {message or ''}".strip())
        self.status, self.data = status, data
