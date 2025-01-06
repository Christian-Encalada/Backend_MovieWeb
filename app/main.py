from fastapi import FastAPI
from app.routers import user, user_classification, recommendations

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(user_classification.router, prefix="/user_classification", tags=["user_classification"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Movie Recommendation API"}