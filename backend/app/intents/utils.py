from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models

def _normalize_for_query(column):
    """
    Creates a SQLAlchemy clause to lowercase a column and remove spaces and periods.
    """
    return func.lower(func.replace(func.replace(column, '.', ''), ' ', ''))

def get_college_by_name(db: Session, college_name: str) -> models.College | None:
    """
    Finds a college by its name, ignoring case, spaces, and periods.
    """
    if not college_name:
        return None
    
    normalized_name = college_name.lower().replace('.', '').replace(' ', '')
    
    return db.query(models.College).filter(
        _normalize_for_query(models.College.name).ilike(f"%{normalized_name}%")
    ).first()
