from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, movie, recommendations

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(movie.router, prefix="/movies", tags=["movies"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Movie Recommendation API"}