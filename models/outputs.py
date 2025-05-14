from dataclasses import dataclass, asdict
from typing import Optional, Dict

@dataclass
class SearchOutput:
    status: str
    file: Optional[str] 
    image_base64: Optional[str]
    query: Dict
    message: Optional[str] = None

    def to_clean_dict(self):
       
        return {key: value for key, value in asdict(self).items() if value is not None}

