from pydantic import BaseModel
from typing import List, Optional


class AskResponse(BaseModel):
    answer: str
    sources: Optional[List[dict]] = None # optional: include retrieved chunks