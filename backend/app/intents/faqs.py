from app import models

def handle_faq_query(params, db):
    question = params.get("question")
    college_name = params.get("college")

    college = db.query(models.College).filter(
        models.College.name.ilike(f"%{college_name}%")
    ).first()

    if not college:
        return f"Sorry, I couldn’t find {college_name}."

    faq = db.query(models.FAQ).filter_by(
        college_id=college.id,
        question=question
    ).first()

    if not faq:
        return f"Sorry, I don’t have an answer for that FAQ at {college.name}."

    return faq.answer
