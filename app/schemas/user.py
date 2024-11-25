from typing import Optional
from pydantic import BaseModel, EmailStr, constr

class UserBase(BaseModel):
    email: EmailStr
    company_name: str
    business_type: str
    country: str
    phone: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_configured: bool = False
    
    class Config:
        from_attributes = True

# Schema para a configuração do perfil
class BusinessConfig(BaseModel):
    description: str
    working_days: list[str]  # Ex: ["MONDAY", "TUESDAY"]
    opening_time: str  # Ex: "09:00"
    closing_time: str  # Ex: "18:00"
    profile_image: Optional[str] = None
    
class BusinessConfigResponse(BusinessConfig):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True