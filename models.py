from sqlalchemy import Column,Integer,String,VARCHAR,BigInteger
from database import Base

class Staff(Base):
    __tablename__="staff"
    
    staff_id = Column(Integer,primary_key=True,index=True)
    name = Column(String(300))
    email=Column(String(300),unique=True)
    phone_number = Column(String(700))
    password = Column(String(300))
    