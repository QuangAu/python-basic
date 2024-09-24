from pydantic import BaseModel, Field


class UserViewModel(BaseModel):
    name: str
    login_id: str
    is_admin: bool
    is_active: bool


class UserModel(BaseModel):
    name: str = Field(max_length=50, min_length=5)
    login_id: str = Field(max_length=50, min_length=5)
    password: str = Field(min_length=6)
    is_admin: bool = Field()
    is_active: bool = Field()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "login_id": "admin-jd",
                "password": "password",
                "is_admin": False,
                "is_active": True,
            }
        }


class UpdateUserModel(BaseModel):
    name: str = Field(max_length=50, min_length=5)
    is_admin: bool = Field()
    is_active: bool = Field()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "is_admin": False,
                "is_active": True,
            }
        }
