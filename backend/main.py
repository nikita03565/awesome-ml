from api.predictions.predictions_api import router
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(router)
