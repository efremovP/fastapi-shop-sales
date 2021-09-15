from pydantic import BaseModel

class GreetFrom(BaseModel):
    name: str