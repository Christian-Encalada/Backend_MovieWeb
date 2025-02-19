from mangum import Mangum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, movie, recommendations, favorite, chat

app = FastAPI()

# Configuración de CORS actualizada
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://frontend-movie-web.vercel.app",  # Agrega tu dominio de producción
    "https://*.vercel.app"  # Permite todos los subdominios de vercel.app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600
)

# Montar los routers
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(movie.router, prefix="/api/movies", tags=["movies"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])
app.include_router(favorite.router, prefix="/api/favorites", tags=["favorites"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/api")
async def root():
    return {"message": "Welcome to the Movie Recommendation API"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Handler for Vercel
handler = Mangum(app)