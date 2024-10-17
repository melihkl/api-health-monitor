from sqlalchemy.orm import Session
from . import models


def create_api(db: Session, api_data: dict):
    db_api = models.API(**api_data)
    db.add(db_api)
    db.commit()
    db.refresh(db_api)
    return db_api


def get_apis(db: Session):
    return db.query(models.API).all()
