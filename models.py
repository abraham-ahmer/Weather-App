from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    
class UserResponse(BaseModel):
    id: int
    username:str
    email:EmailStr
    password:str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes=True



class UserDefaultCity(BaseModel):
    default_city:str
    

class WeatherCreate(BaseModel):

    city:str
class WeatherResponse(BaseModel):
    id: int
    city:str
    current_temp:float
    feels_like:float
    minimum_temp:float
    maximum_temp:float
    checked_at: datetime
    
    user_id: int
    class Config:
        from_attributes=True


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int] = None


class Unit(str, Enum):
    metric = "metric"      # Celsius
    imperial = "imperial"  # Fahrenheit
    standard = "standard"  # Kelvin







