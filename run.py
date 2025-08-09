import os
import uvicorn

# Import the FastAPI app so that Vercel can detect it
from app.main import app

if __name__ == "__main__":
    # Local & Railway execution
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("run:app", host="0.0.0.0", port=port)
