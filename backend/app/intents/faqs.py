from sqlalchemy.orm import Session
from app import models
from app.intents.utils import get_college_by_name

def handle_faq_query(params: dict, db: Session) -> str:
    question = params.get("question")
    college_name = params.get("college")

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn’t find a college named '{college_name}'."

    faq = db.query(models.FAQ).filter_by(
        college_id=college.id,
        question=question
    ).first()

    if not faq:
        return f"Sorry, I don’t have an answer for that FAQ at {college.name}."

    return faq.answer

