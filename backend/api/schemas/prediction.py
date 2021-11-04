from pydantic import BaseModel


class RatingResponse(BaseModel):
    rating: int
