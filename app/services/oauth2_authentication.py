import jwt
import requests
from azure.identity import ClientSecretCredential
from fastapi import Depends
from fastapi_azure_auth.auth import SingleTenantAzureAuthorizationCodeBearer
from schemas.user import User
from settings import (APP_CLIENT_ID, OPENAPI_CLIENT_ID, OPENAPI_CLIENT_SECRET,
                      TENANT_ID)

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=APP_CLIENT_ID,
    tenant_id=TENANT_ID,
    scopes={f"api://{APP_CLIENT_ID}/user_impersonation": "user_impersonation"}
)


def oauth_token_interceptor(token: str = Depends(azure_scheme)) -> User:
    token_data = jwt.decode(token.access_token, options={"verify_signature": False})
    group_id = token_data["groups"][0]
    group_name = get_security_group_name_by_id(group_id)
    user = User()
    user.login_id = token_data["sub"]
    user.is_admin = group_name == "app-admin"
    return user


def get_security_group_name_by_id(group_id):
    # Create a credential object using DefaultAzureCredential
    credential = ClientSecretCredential(TENANT_ID, OPENAPI_CLIENT_ID, OPENAPI_CLIENT_SECRET)

    token = credential.get_token("https://graph.microsoft.com/.default")
    headers = {
        "Authorization": f"Bearer {token.token}"
    }

    url = f"https://graph.microsoft.com/v1.0/groups/{group_id}"
    response = requests.get(url, headers=headers)
    group_data = response.json()
    group_name = group_data.get("displayName")

    return group_name
    return group_name
