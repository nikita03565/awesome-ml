from typing import Any

from api.predictions.calc_predictions import get_rating_prediction
from api.schemas.prediction import RatingRequest, RatingResponse
from fastapi import APIRouter

router = APIRouter()


@router.post("/predict_rating", response_model=RatingResponse)
def predict_rating(body: RatingRequest) -> Any:
    prediction = get_rating_prediction(body.text)
    return RatingResponse(rating=prediction)
