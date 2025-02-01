from typing import List
from pydantic import BaseModel


class PayloadCreateRequest(BaseModel):
    list_1: List[str]
    list_2: List[str]


class PayloadCreateResponse(BaseModel):
    payload_id: int
    message: str


class PayloadReadResponse(BaseModel):
    output: str
