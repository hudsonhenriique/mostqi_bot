from pydantic import BaseModel
from typing import Optional, Dict

class SearchOutput(BaseModel):
    status: str
    file: Optional[str]
    image_base64: Optional[str]
    query: Dict[str, Optional[str]]
    message: Optional[str] = None


