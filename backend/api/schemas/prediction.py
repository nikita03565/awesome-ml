from pydantic import BaseModel


class RatingResponse(BaseModel):
    rating: int


class RatingRequest(BaseModel):
    text: str
