from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, movie, recommendations, favorite, chat

app = FastAPI()

# Configuración de CORS actualizada para Vercel
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://*.vercel.app",
    "https://fronted-movie-web-git-main-christian-encaladas-projects.vercel.app",
    "https://cinexpress.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporalmente permitir todos los orígenes para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar los routers
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(movie.router, prefix="/movies", tags=["movies"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
app.include_router(favorite.router, prefix="/favorites", tags=["favorites"])
app.include_router(chat.router, prefix="/chat", tags=["chat"]) 

@app.get("/")
async def root():
    return {"message": "Welcome to the Movie Recommendation API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/charli")
async def health_check():
    return {"te amo": ":3"}