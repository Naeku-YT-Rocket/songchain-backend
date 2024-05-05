from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer

from src.config.settings import get_settings

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )

settings = get_settings()

class Auth:

    @classmethod
    def jwks_client(cls) -> jwt.PyJWKClient:
        jwks_url = f'https://{settings.auth0_domain}/.well-known/jwks.json'
        return jwt.PyJWKClient(jwks_url)
    
    @classmethod
    async def get_user_id(cls, payload):

        user_info = payload.get('user_info')

        if not user_info:
            raise HTTPException(400, 'user_info not provided')
                    
        user_id = user_info.get('id')

        if not user_id: 
            raise HTTPException(400, 'user_id not provided')

        return user_id

    @classmethod
    async def validate(cls,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(
            HTTPBearer()
        )
    ) -> dict:
        if token is None:
            raise UnauthenticatedException
        
        try:
            jwks_client = cls.jwks_client()
            signing_key = jwks_client.get_signing_key_from_jwt(
                token.credentials
            ).key

        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=settings.auth0_algorithms, # type: ignore
                issuer=settings.auth0_issuer,
                options={
                    'verify_aud': False,
                    'verify_iss': True,
                    'verify_sub': True,
                    'require_exp': True,
                }
            )
        except Exception as error:
            raise UnauthorizedException(str(error))
        
        return payload

    @classmethod
    def _check_claims(cls, payload, claim_name, expected_value):
        # if settings.auth in payload.get('sub', ''):
        #     return True

        if claim_name not in payload:
            raise UnauthorizedException(
                detail=f'No claim <{claim_name}> found in token')

        if not len(expected_value):
            return True

        payload_claim = payload[claim_name]

        authorize = False

        for value in expected_value:
            if value in payload_claim:
                authorize = True


        if not authorize:
            raise UnauthorizedException(detail=f'Missing <{",".join(expected_value)}> scope')
        
        return True
