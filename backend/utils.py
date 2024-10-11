import logging
import os

import boto3
from botocore.exceptions import ClientError
from openai import OpenAI
from passlib.context import CryptContext

from backend.config import settings
from frontend.utils.fs_utils import LOCAL_EXTRACTS_DIRECTORY

LOCAL_EXTRACTS_DIRECTORY = os.path.join("resources", "extracts")

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.OPENAI_KEY)


def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)


def get_s3_client():
    return boto3.client("s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name=settings.AWS_REGION)


def download(key: str):
    s3_client = get_s3_client()
    filename = os.path.basename(key)
    try:
        _ = s3_client.head_object(Bucket=settings.AWS_S3_BUCKET, Key=key)
        s3_client.download_file(
            settings.AWS_S3_BUCKET,
            key,
            os.path.join(LOCAL_EXTRACTS_DIRECTORY, filename),
        )
        logger.info(f"Downloaded file {key} from S3")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":  # File not found
            logger.error(f"File {key} not found on S3")
            return False
        else:
            logger.error("")
            return False


def load_file_contents(key: str) -> str:
    ensure_directory_exists(LOCAL_EXTRACTS_DIRECTORY)
    local_path = os.path.join(LOCAL_EXTRACTS_DIRECTORY, os.path.basename(key))

    if not os.path.exists(local_path):
        download(key)
    with open(local_path, "r", encoding="utf-8") as f:
        return f.read()
