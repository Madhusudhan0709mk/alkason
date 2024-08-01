from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from api.routes import router as api_router
from api.auth import router as auth_router

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")

# Serve React app
app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    file_path = f"../frontend/build/{full_path}"
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse("../frontend/build/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)