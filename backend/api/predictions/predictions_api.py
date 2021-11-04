from typing import Any

from fastapi import APIRouter

from api.predictions.calc_predictions import get_rating_prediction
from api.schemas.prediction import RatingResponse

router = APIRouter()


@router.post("/predict_rating", response_model=RatingResponse)
def predict_rating(
        article_text
) -> Any:
    prediction = get_rating_prediction(article_text)
    return RatingResponse(rating=prediction)
