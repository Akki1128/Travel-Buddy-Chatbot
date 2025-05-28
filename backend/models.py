from pydantic import BaseModel, Field # type: ignore
from typing import List, Literal, Optional

#Defines a single message in the chat history
class Message(BaseModel):
    role: Literal["user","model"]
    parts: List[str]

# Defines the structure of the request coming from the frontend
class ChatRequest(BaseModel):
    message: str
    history: List[Message] = Field(default_factory=list)

# Defines the structure of the response sent to the frontend
class ChatResponse(BaseModel):
    response: str

