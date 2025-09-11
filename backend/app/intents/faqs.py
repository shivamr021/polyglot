from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from app.intents.utils import get_college_by_name, _normalize_for_query

def handle_faq_query(params: dict, db: Session) -> str:
    college_name = params.get("college")
    query_text = params.get("query_text")

    if not college_name:
        return "Please specify a college to ask a question."

    if not query_text:
        return "What would you like to ask?"

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn’t find a college named '{college_name}'."

    # Normalize the user's query text
    normalized_query = query_text.lower().replace('.', '').replace(' ', '').replace('?', '')

    # Find the most relevant FAQ using the normalized search
    faq = (
        db.query(models.FAQ)
        .filter(
            models.FAQ.college_id == college.id,
            _normalize_for_query(models.FAQ.question).ilike(f"%{normalized_query}%"),
        )
        .first()
    )

    if not faq:
        return f"I'm sorry, I couldn't find an answer for '{query_text}' at {college.name}. Please try rephrasing your question."

    return faq.answer

