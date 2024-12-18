from typing import Optional

from pydantic import BaseModel


class APICreate(BaseModel):
    name: str
    url: str
    method: str
    params: Optional[str] = None
    cookie: Optional[str] = None
