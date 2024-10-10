from datetime import datetime

from sqlalchemy import Column, String, Integer, func, TIMESTAMP, VARCHAR, DateTime

from backend.database import Base

from backend.database import db_session

# class PdfExtractions(Base):
#     __tablename__ = 'pdf_extractions'
#
#     id = Column(Integer, primary_key=True)
#     filename = Column(String(255), nullable=False)
#     s3_bucket = Column(VARCHAR(63), nullable=False)
#     s3_key = Column(VARCHAR(1024), nullable=False)
#     s3_media_key = Column(VARCHAR(1024), nullable=True)
#     extraction_status = Column(String(20), nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), default=func.current_timestamp())
#     updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.current_timestamp(), default=func.current_timestamp())

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


# Function to create a new PDF extraction record
def create_pdf_extraction(filename: str, s3_bucket: str, s3_key: str, extraction_status: str, s3_media_key: str = None):
    with db_session() as session:
        new_extraction = PdfExtractions(
            filename=filename,
            s3_bucket=s3_bucket,
            s3_key=s3_key,
            extraction_status=extraction_status,
            s3_media_key=s3_media_key,
        )
        session.add(new_extraction)
        session.commit()
        return new_extraction
    
# Function to fetch PDF extraction data from the database
def fetch_pdf_extractions():
    with db_session() as session:
        extractions = session.query(PdfExtractions).all()
        return extractions