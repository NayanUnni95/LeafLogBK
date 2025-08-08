from datetime import datetime
from typing import Dict, Tuple
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt


from app.core.config import settings
from app.util.date_util import DateUtil
from app.util.types import JWTTokenKey, Algorithm


class JWTUtils:
    """
    Utility class for handling JWT tokens

    Attributes:
    - oauth2_scheme (OAuth2PasswordBearer): OAuth2 password
        bearer scheme for JWT tokens.

    Methods:
    - is_jwt_authenticated(token: str) -> Tuple[None, Dict]:
        Validates and decodes a JWT token.

    - get_current_user(token: str = Depends on(oauth2_scheme)) -> Dict:
        Retrieves the current user's payload from a JWT token.


    """
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    async def is_jwt_authenticated(token: str) -> Tuple[None, Dict]:
        """
        Validates and decodes a JWT token.

        Parameters:
        - token (str): JWT token.

        Returns:
        - Tuple[None, Dict]: None if authenticated, decoded payload otherwise.
        """
        try:
            if not token:
                raise HTTPException(status_code=401 ,detail={
                    "hasError": True,
                    "statusCode": 1000,
                    "message": "Empty Token",
                    "response": {}
                })
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[Algorithm.HS256.value])
            user_id = payload.get(JWTTokenKey.ID.value)
            expiry = datetime.strptime(payload.get(JWTTokenKey.EXPIRY.value), '%Y-%m-%d %H:%M:%S.%f%z')

            if not user_id or expiry < DateUtil.get_current_time():
                raise HTTPException(status_code=401, detail={
                    "hasError": True,
                    "statusCode": 1000,
                    "message": "Token Or Invalid",
                    "response": {},
                })
            if payload.get(JWTTokenKey.PRODUCT_NAME.value) != settings.PROJECT_NAME:
                raise HTTPException(status_code=401, detail={
                    "hasError": True,
                    "statusCode": 1000,
                    "message": "Invalid token",
                    "response": {},
                })

            return None, payload
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail={
                "hasError": True,
                    "statusCode": 1000,
                    "message": "Token has Expired",
                    "response": {}
            })
        
        except jwt.JWTError as e:
            raise HTTPException(status_code=401, detail={
                "hasError": True,
                    "statusCode": 1000,
                    "message": f"JWT Error: {str(e)}",
                    "response": {}
            })
        
    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
        """
        Retrieves the current user's payload from a JWT token.

        Parameters:
        - token (str): JWT token.

        Returns:
        - Dict: Decoded payload.
        """

        _, payload = await JWTUtils.is_jwt_authenticated(token)

        return payload