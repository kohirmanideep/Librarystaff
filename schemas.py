from typing import Optional
from pydantic import BaseModel

class Staff(BaseModel):
    name:str
    email:str
    phone_number:str
    password:str
    
class ShowStaff(BaseModel):
    staff_id:int
    name:str
    email:str
    phone_number:str
    password:str
    
    class Config():
        orm_mode = True
        
class Login(BaseModel):
    username:str
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    email:Optional[str]=None    