from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

from db import db_session

Base = declarative_base()
class PdfExtractionsModel(Base):
    __tablename__ = "pdf_extractions"

    id = Column(name="id", type_=Integer, primary_key=True, autoincrement=True)
    filename = Column(name="filename", type_=String(255), nullable=False)
    s3_bucket = Column(name="s3_bucket", type_=String(63), nullable=False)
    source_file_key = Column(name="source_file_key", type_=String(1024), nullable=False)
    extracted_file_key = Column(name="extracted_file_key", type_=String(1024), nullable=True)
    extracted_media_key = Column(name="extracted_media_key", type_=String(1024), nullable=True)
    extraction_status = Column(
        name="extraction_status", type_=String(20), nullable=False
    )
    extraction_mechanism = Column(name="extraction_mechanism", type_=String(30), nullable=False)
    created_at = Column(name="created_at", type_=DateTime, default=datetime.now())
    modified_at = Column(
        name="modified_at",
        type_=DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
    )


# Function to create a new PDF extraction record
def create_pdf_extraction(
    filename: str,
    s3_bucket: str,
    source_file_key: str,
    extracted_file_key:str,
    extracted_media_key:str,
    extraction_status: str,
    extraction_mechanism: str
    # s3_media_key: str = None,
):
    with db_session() as session:
        new_extraction = PdfExtractionsModel(
            filename=filename,
            s3_bucket=s3_bucket,
            source_file_key=source_file_key,
            extracted_file_key=extracted_file_key,
            extracted_media_key=extracted_media_key,
            extraction_status=extraction_status,
            extraction_mechanism=extraction_mechanism
            # s3_media_key=s3_media_key,
        )
        session.add(new_extraction)
        session.commit()
        return new_extraction


# Function to fetch PDF extraction data from the database
def fetch_all_pdf_extractions():
    with db_session() as session:
        extractions = session.query(PdfExtractionsModel.id, PdfExtractionsModel.filename, PdfExtractionsModel.extraction_mechanism).all()
        return extractions


def get_pdf_extractions_by_mechanism(extraction_mechanism: str):
    with db_session() as session:
        extractions = session.query(PdfExtractionsModel).filter(
            PdfExtractionsModel.extraction_mechanism == extraction_mechanism
        ).all()
        return extractions
