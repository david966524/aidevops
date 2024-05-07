from pydantic import BaseModel, Field

from typing import Any
class Resp(BaseModel):
    HttpCode: int | str = Field(default=None,title="HttpCode", description="HttpCode")
    Data: Any = Field(default=None,title="Data", description="Data")
