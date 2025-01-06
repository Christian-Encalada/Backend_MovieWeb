from pydantic import BaseModel
from typing import List

class UserClassificationResponse(BaseModel):
    user_id: int
    classification: List[str]