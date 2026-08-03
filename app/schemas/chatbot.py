from pydantic import BaseModel
from typing import Optional

class ChatBotBase(BaseModel):
    name: str
    color_theme: Optional[str] = "#000000"
    model_type: Optional[str] = "gpt-3.5-turbo"
    system_prompt: Optional[str] = "Hey there!"
    voice_support: Optional[bool] = False

class ChatBotCreate(ChatBotBase):
    pass

class ChatBotUpdate(BaseModel):
    name: Optional[str] = None
    color_theme: Optional[str] = None
    model_type: Optional[str] = None
    system_prompt: Optional[str] = None
    voice_support: Optional[bool] = None

class ChatBotResponse(ChatBotBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

