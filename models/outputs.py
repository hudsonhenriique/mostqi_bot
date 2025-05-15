from pydantic import BaseModel
from typing import Optional, Dict

class SearchOutput(BaseModel):
    status: str
    file: Optional[str] = None
    image_base64: Optional[str] = None
    query: Dict[str, Optional[str]]
    message: Optional[str] = None




