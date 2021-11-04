import random

def get_rating_prediction(article_text: str) -> int:
    # TODO implement
    prediction = random.randrange(0, len(article_text))
    return prediction