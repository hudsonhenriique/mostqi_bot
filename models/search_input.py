from dataclasses import dataclass
from typing import Optional

@dataclass
class SearchInput:
    name: Optional[str] = None
    cpf: Optional[str] = None
    social_filter: bool = False
