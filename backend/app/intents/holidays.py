from app import models

def handle_holiday_query(params, db):
    college_name = params.get("college")

    college = db.query(models.College).filter(
        models.College.name.ilike(f"%{college_name}%")
    ).first()

    if not college:
        return f"Sorry, I couldn’t find {college_name}."

    holidays = db.query(models.Holiday).filter_by(college_id=college.id).all()

    if not holidays:
        return f"No holidays found for {college.name}."

    holiday_list = ", ".join([h.holiday_name for h in holidays])
    return f"Holidays at {college.name} are: {holiday_list}"
