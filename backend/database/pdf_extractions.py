from datetime import datetime

from sqlalchemy import Column, String, Integer, func, TIMESTAMP, VARCHAR, DateTime

from backend.database import Base


class PdfExtractions(Base):
    __tablename__ = 'pdf_extractions'

    id = Column(name="id", type_=Integer, primary_key=True, autoincrement=True)
    filename = Column(name="filename", type_=String(255), nullable=False)
    s3_bucket = Column(name="s3_bucket", type_=String(63), nullable=False)
    s3_key = Column(name="s3_key", type_=String(1024), nullable=False)
    s3_media_key = Column(name="s3_media_key", type_=String(1024), nullable=True)
    extraction_status = Column(name="extraction_status", type_=String(20), nullable=False)
    created_at = Column(name="created_at", type_=DateTime, default=datetime.now())
    modified_at = Column(name="modified_at", type_=DateTime, default=datetime.now(), onupdate=datetime.now())
