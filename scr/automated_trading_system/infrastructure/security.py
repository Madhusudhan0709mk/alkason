import jwt
from datetime import datetime, timedelta

class Security:
    def __init__(self, config):
        self.config = config
        self.secret_key = config.get('jwt_secret_key')

    def generate_token(self, user_id: str) -> str:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS')