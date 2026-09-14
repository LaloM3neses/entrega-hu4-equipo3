from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.report import ReportCreate, ReportRead
from app.services import report as report_service

router = APIRouter()


@router.post(
    "/",
    response_model=ReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear reporte (version minima, para poder probar HU-4)",
)
def create_report(
    report_in: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Alta minima de incidencias. El formulario completo (HU-05/06) lo entrega
    Equipo 1; este endpoint existe para no bloquear las pruebas de consulta
    y seguimiento (HU-4) mientras tanto.
    """
    return report_service.create_report(db, current_user.id, report_in)


@router.get(
    "/",
    response_model=list[ReportRead],
    summary="Listar incidencias reportadas (HU-4)",
)
def list_reports(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return report_service.list_reports(db)


@router.get(
    "/{folio}",
    response_model=ReportRead,
    summary="Consultar incidencia por folio (HU-4)",
)
def get_report(
    folio: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    report = report_service.get_report(db, folio)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe un reporte con ese folio",
        )
    return report
