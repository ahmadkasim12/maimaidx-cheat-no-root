from typing import Any
from pydantic import BaseModel

class ResponseModel(BaseModel):
    status_code: int
    message: str
    data: Any
    
class ResponseModelObjectId(ResponseModel):
    data: str