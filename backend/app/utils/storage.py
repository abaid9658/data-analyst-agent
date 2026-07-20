"""
Storage utilities for MinIO / S3 compat object storage
"""
import io
import logging
import os
import boto3
from botocore.client import Config
from app.config import settings

logger = logging.getLogger(__name__)

# Initialize S3 client for MinIO
def get_s3_client():
    # Allow local folder fallback if MinIO endpoint is not configured or configured as local
    if not settings.MINIO_ENDPOINT or settings.MINIO_ENDPOINT == "local":
        return None

    return boto3.client(
        "s3",
        endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )


async def upload_file_to_storage(content: bytes, filename: str) -> str:
    """Upload content to S3/MinIO bucket. Fallback to local file if not configured."""
    client = get_s3_client()
    if client is None:
        # Local filesystem storage fallback
        local_path = os.path.join("storage", filename)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(content)
        logger.info("Saved file locally to %s", local_path)
        return local_path

    try:
        # Ensure bucket exists
        try:
            client.head_bucket(Bucket=settings.MINIO_BUCKET)
        except Exception:
            client.create_bucket(Bucket=settings.MINIO_BUCKET)

        # Upload
        client.put_object(
            Bucket=settings.MINIO_BUCKET,
            Key=filename,
            Body=content,
        )
        logger.info("Uploaded file to MinIO: %s", filename)
        return filename
    except Exception as e:
        logger.error("Failed to upload to object storage: %s. Saving locally.", e)
        # Fallback to local
        local_path = os.path.join("storage", filename)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(content)
        return local_path


async def download_file_from_storage(storage_path: str) -> bytes:
    """Download content from S3/MinIO bucket or local filesystem."""
    client = get_s3_client()
    if client is None or not os.path.exists(storage_path) if "/" not in storage_path else False:
        # Check if local file exists
        if os.path.exists(storage_path):
            with open(storage_path, "rb") as f:
                return f.read()

    try:
        response = client.get_object(Bucket=settings.MINIO_BUCKET, Key=storage_path)
        return response["Body"].read()
    except Exception as e:
        # Fallback to check local file if it fails
        local_path = os.path.join("storage", storage_path)
        if os.path.exists(local_path):
            with open(local_path, "rb") as f:
                return f.read()
        logger.error("Failed to download file from storage: %s", e)
        raise FileNotFoundError(f"Storage path {storage_path} not found") from e


async def delete_file_from_storage(storage_path: str) -> None:
    """Delete a file from S3/MinIO or local filesystem."""
    client = get_s3_client()
    if client is None:
        if os.path.exists(storage_path):
            os.remove(storage_path)
        return

    try:
        client.delete_object(Bucket=settings.MINIO_BUCKET, Key=storage_path)
    except Exception as e:
        logger.error("Failed to delete file from storage: %s", e)
