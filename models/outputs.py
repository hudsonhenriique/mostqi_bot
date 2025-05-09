from dataclasses import dataclass
from typing import Optional, Dict

@dataclass

class SearchOutput:
    status: str
    arquivo: Optional[str] 
    imagem_base64: Optional[str]
    consulta: Dict
    mensagem: Optional[str] = None
    