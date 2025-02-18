# Movie User Classification System

A FastAPI-based API for classifying users based on their movie preferences and providing personalized recommendations.

## Features

- User authentication and authorization
- Movie preference classification
- Personalized movie recommendations
- Movie search and details
- User favorite management
- Docker containerization
- PostgreSQL database integration

## Requirements

- Python 3.8+
- PostgreSQL
- Docker and Docker Compose
- TMDB API key

## Installation

1. Clone the repository:
```sh
git clone <repository_url>
cd backend
```

2. Create a `.env` file with the following environment variables:
```properties
# Database Settings
DB_USER=proyecto_ia
DB_PASSWORD=Pucem.2024
DB_HOST=proyecto-ia-pucem.postgres.database.azure.com
DB_PORT=5432
DB_NAME=postgres

# JWT Settings
secret_key=your_secret_key
algorithm=HS256
access_token_expire_minutes=1440

# TMDB Settings
TMDB_API_KEY=your_tmdb_api_key
```

3. Build and start the Docker containers:
```sh
docker-compose up --build -d
```

4. Run database migrations:
```sh
# Execute migrations inside the container
docker exec backend-web-1 alembic upgrade head

# For creating new migrations
docker exec backend-web-1 alembic revision --autogenerate -m "migration_name"
```

## Development

### Running the Application

1. Start the development server:
```sh
docker-compose up
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Project Structure
```
backend/
├── app/
│   ├── models/          # Database models
│   ├── routers/         # API routes
│   ├── schemas/         # Pydantic models
│   ├── services/        # Business logic
│   ├── utils/          # Utility functions
│   └── main.py         # Application entry point
├── alembic/            # Database migrations
├── tests/             # Unit tests
├── docker-compose.yml  # Docker configuration
├── Dockerfile         # Docker build instructions
└── requirements.txt   # Python dependencies
```

## API Endpoints

### User Management
- `POST /users/register` - Register new user
- `POST /users/login` - User login
- `GET /users/profile` - Get user profile
- `PUT /users/update` - Update user information

### Movies
- `GET /movies/` - List movies
- `GET /movies/{id}` - Get movie details
- `GET /movies/search` - Search movies
- `POST /movies/favorites` - Add to favorites
- `DELETE /movies/favorites/{id}` - Remove from favorites

### Recommendations
- `GET /recommendations/` - Get personalized recommendations
- `POST /recommendations/update` - Update user preferences

## Database Management

### Creating Migrations
```sh
docker exec backend-web-1 alembic revision --autogenerate -m "migration_description"
```

### Applying Migrations
```sh
docker exec backend-web-1 alembic upgrade head
```

## Testing

Run the test suite:
```sh
docker exec backend-web-1 pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Christian Encalada
- Contributors

## Acknowledgments

- FastAPI
- SQLAlchemy
- TMDB API
- PostgreSQL