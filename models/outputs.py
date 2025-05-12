from dataclasses import dataclass
from typing import Optional, Dict

@dataclass

class SearchOutput:
    status: str
    file: Optional[str] 
    image_base64: Optional[str]
    query: Dict
    mensage: Optional[str] = None
    