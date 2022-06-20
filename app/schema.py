from pydantic import BaseModel
from datetime import datetime
from typing import List


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: int


class Block(BaseModel):
    index: int
    timestamp: datetime
    transactions: List[Transaction]
    previous_hash: str
    proof: int
