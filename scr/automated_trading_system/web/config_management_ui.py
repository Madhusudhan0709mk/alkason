from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Dict, Any

class ConfigManagementUI:
    def __init__(self, config, security):
        self.app = FastAPI()
        self.config = config
        self.security = security
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/token")
        async def login(form_data: OAuth2PasswordRequestForm = Depends()):
            user = await self.authenticate_user(form_data.username, form_data.password)
            if not user:
                raise HTTPException(status_code=400, detail="Incorrect username or password")
            access_token = self.security.generate_token(user['id'])
            return {"access_token": access_token, "token_type": "bearer"}

        @self.app.get("/config")
        async def get_config(token: str = Depends(self.security.oauth2_scheme)):
            user = self.security.verify_token(token)
            return self.config.get_all()

        @self.app.post("/config")
        async def update_config(config: Dict[str, Any], token: str = Depends(self.security.oauth2_scheme)):
            user = self.security.verify_token(token)
            # Implement config update logic
            pass

    async def authenticate_user(self, username: str, password: str):
        # Implement user authentication logic
        pass

    async def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
