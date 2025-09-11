from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import csv
import io
import logging

from app import models, schemas, auth
from app.database import get_db

logger = logging.getLogger(__name__)

# Create a new router for all upload-related endpoints
router = APIRouter(
    prefix="/upload",
    tags=["Bulk Uploads"],
    # You can secure all routes in this file with a single dependency
    dependencies=[Depends(auth.get_current_active_user)]
)

@router.post("/fees/")
def upload_fees_csv(
    # Use Form(...) to receive the college_id alongside the file
    college_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    # We still need current_user here to check their role
    current_user: schemas.UserOut = Depends(auth.get_current_active_user)
):
    """
    Handles the bulk upload of fees from a CSV file.
    The CSV must contain the headers: 'course_name', 'amount', 'deadline', 'category'.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can upload data.")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")

    try:
        contents = file.file.read()
        buffer = io.StringIO(contents.decode("utf-8"))
        csv_reader = csv.DictReader(buffer)
        
        fees_to_create = []
        errors = []
        expected_headers = {"course_name", "amount", "deadline"}

        if not csv_reader.fieldnames or not expected_headers.issubset(csv_reader.fieldnames):
            raise HTTPException(status_code=400, detail=f"CSV headers are incorrect. Expected at least: {list(expected_headers)}")

        for i, row in enumerate(csv_reader):
            try:
                fee_data = schemas.FeeCreate(
                    college_id=college_id,
                    course_name=row["course_name"],
                    amount=float(row["amount"]),
                    deadline=row["deadline"],
                    category=row.get("category", "General")
                )
                fees_to_create.append(fee_data)
            except Exception as e:
                errors.append(f"Row {i+2}: {e}")

        if errors:
            raise HTTPException(status_code=400, detail={"message": "Validation errors found in CSV", "errors": errors})

        for fee_data in fees_to_create:
            new_fee = models.Fee(**fee_data.dict())
            db.add(new_fee)
        
        db.commit()
        return {"message": f"Successfully uploaded and created {len(fees_to_create)} fee records."}

    except Exception as e:
        db.rollback()
        logger.error(f"Error processing fees CSV: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

# You can add more upload endpoints here later, like upload_faqs_csv, etc.