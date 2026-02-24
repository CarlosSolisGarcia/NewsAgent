# Pydantic models
from datetime import datetime
from pydantic import BaseModel, HttpUrl

class NewsItem(BaseModel):
    title: str
    link: HttpUrl	
    date: datetime | None
    source: str
    summary: str = ""

    model_config = {"from_attributes": True}

    class Config:
        str_strp_whitespace = True

