from sqlalchemy.orm import Session
from app import models

def get_college_by_name(db: Session, college_name: str) -> models.College | None:
    """
    Fetches a college from the database using a case-insensitive partial match.
    """
    if not college_name:
        return None
    return db.query(models.College).filter(
        models.College.name.ilike(f"%{college_name}%")
    ).first()
