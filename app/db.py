"""SQLite-backed activity history using SQLAlchemy 2."""
from pathlib import Path
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from app.config import get_settings

class Base(DeclarativeBase):
    pass

class Inspection(Base):
    __tablename__ = "inspections"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kind: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

def _build_engine():
    url = get_settings().database_url
    if url.startswith("sqlite:///"):
        path = url.removeprefix("sqlite:///")
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url, pool_pre_ping=True)

engine = _build_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def init_db() -> None:
    Base.metadata.create_all(bind=engine)

def record_inspection(kind: str, subject: str) -> None:
    with SessionLocal() as session:
        session.add(Inspection(kind=kind, subject=subject[:500]))
        session.commit()

def recent_inspections(limit: int = 10) -> list[Inspection]:
    with SessionLocal() as session:
        return list(session.scalars(select(Inspection).order_by(Inspection.id.desc()).limit(limit)))
