from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models
from app.auth.roles import require_role
from app.services import report_service


router = APIRouter(
    prefix = '/reports',
    tags = ['Reports']
)

@router.get('/dashboard')
def dashboard(db: Session = Depends(get_db), user = Depends(require_role(['ADMIN', 'RECEPCIONIST']))):
    return report_service.get_dashaboard_data(db)