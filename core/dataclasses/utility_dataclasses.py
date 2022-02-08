from datetime import datetime

from pydantic import BaseModel


class VDRServiceError(BaseModel):
    error: bool = 1
    message: str
    status_code: int
    endpoint: str
    timestamp: datetime
