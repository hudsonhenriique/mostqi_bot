from pydantic import BaseModel
from typing import Optional

class SearchOutput(BaseModel):
    status: str
    file: Optional[str] = None
    image_base64: Optional[str] = None
    file_drive_url: Optional[str] = None
    screenshot_drive_url: Optional[str] = None
    sheet_append_status: Optional[str] = None
    query: dict
    message: Optional[str] = None