from mangum import Mangum
from app.main import app

# Create handler for AWS Lambda / Vercel
handler = Mangum(app, lifespan="off")