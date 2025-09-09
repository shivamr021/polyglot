from app import models

def handle_fee_deadline(params, db):
    course = params.get("course")
    college_name = params.get("college")

    college = db.query(models.College).filter(
        models.College.name.ilike(f"%{college_name}%")
    ).first()

    if not college:
        return f"Sorry, I couldn’t find {college_name}."

    fee = db.query(models.Fee).filter_by(
        college_id=college.id,
        program=course
    ).first()

    if not fee:
        return f"Sorry, I couldn’t find fee details for {course} at {college.name}."

    deadline = fee.deadline.strftime("%d-%b-%Y")
    return f"The fee deadline for {course} at {college.name} is {deadline}. Amount: INR {fee.amount}."
