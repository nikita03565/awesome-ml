from predictor.predict import get_prediction

def get_rating_prediction(article_text: str) -> int:
    return get_prediction(article_text)
