from sqlalchemy.orm import Session
from sqlmodel import select

from app.models.report import Report
from app.schemas.report import ReportCreate


def create_report(db: Session, author_id: int, report_in: ReportCreate) -> Report:
    report = Report(
        title=report_in.title,
        description=report_in.description,
        campus_label=report_in.campus_label,
        space_label=report_in.space_label,
        image_url=report_in.image_url,
        author_id=author_id,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def list_reports(db: Session) -> list[Report]:
    return list(db.scalars(select(Report).order_by(Report.id.desc())).all())


def get_report(db: Session, folio: int) -> Report | None:
    return db.get(Report, folio)
