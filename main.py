from fastapi import FastAPI,Depends
import schemas,models
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from database import engine
from typing import List
from fastapi import status,HTTPException
from hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm
import Token,oauth2
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from jose import JWTError,jwt

models.Base.metadata.create_all(engine)

app=FastAPI()

origins = [  "http://127.0.0.1",
    "http://localhost",
    "http://localhost:3000/"
    "http://127.0.0.1:3000/",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://localhost:3000/Libraryregister",
    "http://localhost:3000/Libraryregister",
    "http://localhost:8000",
    "http://localhost:8000/members",
    "http://localhost:3000/Staffprofile"
    "http://127.0.0.1:8001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post('/staff',response_model=schemas.ShowStaff,tags = ['staff'])
def create_staff(request:schemas.Staff,db:Session=Depends(get_db)):
    new_staff=models.Staff(name=request.name,email=request.email,phone_number=request.phone_number,password=Hash.bcrypt(request.password))
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    db.close()
    return new_staff

@app.post('/login',tags=['staff'])
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    staff=db.query(models.Staff).filter(models.Staff.email==request.username).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    if not Hash.verify(staff.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    access_token = Token.create_access_token(data={"sub":staff.email})
    return {"access_token":access_token,"token_type":"bearer"}
 
@app.get('/get/staff/{staff_id}',response_model=schemas.ShowStaff,tags=['staff'])
def get_member(staff_id,db:Session=Depends(get_db)):
    staff=db.query(models.Staff).filter(models.Staff.staff_id == staff_id).first()
    return staff

@app.get('/staff/',response_model=List[schemas.ShowStaff],tags=['staff'])
def get_member(db:Session=Depends(get_db)):
    staff=db.query(models.Staff).all()
    return staff

@app.put('/staff/{staff_id}',status_code=status.HTTP_404_NOT_FOUND,tags = ['staff'])
def create_member(staff_id,request:schemas.Staff,db:Session=Depends(get_db)):
    db.query(models.Staff).filter(models.Staff.staff_id==staff_id).update(request.dict)
    db.commit()
    return 'updated'

@app.delete('/staff/{staff_id}',status_code=status.HTTP_404_NOT_FOUND,tags = ['staff'])
def create_staff(staff_id,db:Session=Depends(get_db)):
    db.query(models.Staff).filter(models.Staff.staff_id==staff_id).delete(synchronize_session=False)
    db.commit()
    return 'DONE'


@app.post("/decoder", tags=['decoder'])
def verify_token(token:str, db:Session=Depends(get_db)):
        payload = jwt.decode(token, Token.SECRET_KEY, algorithms=[Token.ALGORITHM])
        email: str = payload.get("sub")  
        if email is None:
            raise HTTPException(status_code=404,detail="token not decoded")
        token_data = schemas.TokenData(email=email)
        return db.query(models.Staff).filter(models.Staff.email==email).first()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
