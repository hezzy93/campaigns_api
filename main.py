from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, get_db
import schemas, crud, models
from typing import List
from schemas import TokenData
from auth import create_access_token, verify_password,settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from uuid import UUID
from datetime import datetime, timezone

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campaign API", version="1.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users_Login")

@app.post("/users_Login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.id is None:
        raise ValueError("User ID is missing from database!")  
    
    access_token = create_access_token(data={"sub": user.email, "id": str(user.id)})  
    return {"access_token": access_token, "token_type": "bearer"}


# Dependency to get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user_id: UUID = UUID(payload.get("id"))
        if email is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(sub=email, id=user_id)

    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    if user is None:
        raise credentials_exception

    return user

# Endpoint to Enroll new user
@app.post("/users/enroll", tags=["User"])
def enroll(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = crud.add_user(db=db, user=user)
    return {"message": "User created successfully", "user_id": str(created_user.id)}

# Endpoint to CREATE Campaign
@app.post("/api/campaigns/", tags=["Campaign"])
def create_campaign(
    campaign: schemas.CampaignCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.TokenData = Depends(get_current_user)
):
    added_campaign = crud.add_campaign(db, campaign, current_user.id)
    return {"campaign": added_campaign}


# Endpoint to READ ALL Campaigns
@app.get("/api/campaigns/", response_model=List[schemas.CampaignOutputResponse], tags=["Campaign"])
def get_campaigns(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    pageSize: int = Query(20, ge=1, le=100, description="Number of items per page")
):
    offset = (page - 1) * pageSize
    campaigns = crud.get_campaigns(db, offset=offset, limit=pageSize)
    return campaigns

# Endpoint to GET Campaign by id
@app.get("/api/campaigns/{campaign_id}", response_model=schemas.CampaignOutputResponse, tags=["Campaign"])
def get_campaign_by_id(campaign_id: UUID, db: Session = Depends(get_db)):
    campaign = crud.get_campaign_by_id(db=db, campaign_id=campaign_id)
    if campaign is None:
       raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign 

# Endpoint to UPDATE campaigns
@app.put("/api/campaigns/{campaign_id}", tags=["Campaign"])
def update_campaign(campaign_id: UUID, payload: schemas.CampaignUpdate, db:Session= Depends(get_db)):
    updated_campaign = crud.update_campaign(
        db=db,
        campaign_id=campaign_id,
        campaign_update=payload
    )
    if updated_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign updated successfully", "campaign": updated_campaign}


# Endpoint to DELETE a Campaign by Id
@app.delete("/api/campaigns/{campaign_id}", tags=["Campaign"])
def delete_campaign(campaign_id:UUID, db: Session = Depends(get_db)):
    result = crud.delete_campaign(db,campaign_id)

    if "error" in result:
      raise HTTPException(status_code=404, detail=result["error"])

    return result
    