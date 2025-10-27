from fastapi import HTTPException
from sqlalchemy.orm import Session
import schemas, models
from auth import hash_password
from uuid import UUID

# Create User
def add_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get User by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email.ilike(email)).first()



# Function to CREATE Campaign
def add_campaign(db: Session, campaign: schemas.CampaignCreate, user_id: int):
    db_campaign = models.Campaign(
        name = campaign.name,
        description = campaign.description,
        start_date = campaign.start_date,
        end_date = campaign.end_date,
        budget = campaign.budget,
        created_by = user_id
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

# Function to GET ALL Campaigns
def get_campaigns(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.Campaign).offset(offset).limit(limit).all()

# Function to GET Campaigns by ID
def get_campaign_by_id(db: Session, campaign_id: UUID):
    return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()


#Function to Update Campaign
def update_campaign(db:Session, campaign_id:UUID, campaign_update: schemas.CampaignUpdate):
    db_campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not db_campaign:
        return None
    
    for key, value in campaign_update.model_dump(exclude_unset=True).items():
        setattr(db_campaign, key, value)

    db.commit()
    db.refresh(db_campaign)
    return db_campaign


# Function to DELETE Campaign
def delete_campaign(db: Session, campaign_id: UUID):
    db_campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()

    if not db_campaign:
        return {"error": "Campaign not found"}
    
    db.delete(db_campaign)
    db.commit()
    return{"message": f"Campaign {campaign_id} deleted successfully."}