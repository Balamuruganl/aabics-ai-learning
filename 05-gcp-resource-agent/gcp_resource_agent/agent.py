import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage
from google.adk.agents import LlmAgent

load_dotenv()
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = os.environ["GCP_REGION"]
DATASET_ID = os.environ["BQ_DATASET"]
TABLE_ID = os.environ["BQ_TABLE"]
#BUCKET_NAME = os.environ["GCS_BUCKET"]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
print (f"PROJECT_ROOT: {PROJECT_ROOT}")

CSV_FILE = PROJECT_ROOT / "data" / "products.csv"

def create_gcs_bucket(BUCKET_NAME) -> dict:
    """Create the configured private Cloud Storage bucket if needed."""
    client = storage.Client(project=PROJECT_ID)
    bucket = client.lookup_bucket(BUCKET_NAME)
    if bucket:
        return {
            "status": "exists",
            "bucket": BUCKET_NAME,
            "message": "Bucket already exists."
        }    
    
    bucket = client.create_bucket(
        BUCKET_NAME,
        project=PROJECT_ID,
        location=REGION,
        )

    return {
        "status": "created",
        "bucket": bucket.name,
        "location": bucket.location,
    }


def upload_file_to_bucket(BUCKET_NAME) -> dict:
    """Upload the project's products.csv file to the configured GCS bucket."""
    if not CSV_FILE.is_file():
        return {
            "status": "error",
            "message": f"CSV file not found: {CSV_FILE}"
        }

    client = storage.Client(project=PROJECT_ID)
        # Retrieve the actual Bucket object
    bucket = client.lookup_bucket(BUCKET_NAME)

    if bucket is None:
        return {
            "status": "error",
            "message": "Bucket does not exist. Create it first."
        }

    blob = bucket.blob("products.csv")
    blob.upload_from_filename(
        str(CSV_FILE),
        content_type="text/csv",
    )

    return {
        "status": "uploaded",
        "bucket": BUCKET_NAME,
        "object": "products.csv",
        "gs_uri": f"gs://{BUCKET_NAME}/products.csv",
    }

root_agent = LlmAgent(
    name="gcp_resource_agent",
    model="gemini-3.5-flash-lite",
    description="An agent that manages selected GCP Storage resources.",
    instruction=f"""
You are a GCP resource management assistant.

Use the provided tools to perform these tasks:
1. Create any Cloud Storage bucket.
2. Upload products.csv to the specified bucket only when asked.


Rules:
- Execute operations in the correct order.
- Before uploading, ensure the bucket exists.
- Report the actual result returned by each tool.
- Never claim an operation succeeded if the tool reports an error.
- If a tool fails, explain the error and do not claim later steps succeeded.
- Ask for clarification if the user's request is ambiguous.
- Do not delete resources or change IAM permissions.

Configuration:
GCP project: {PROJECT_ID}



""",
    tools=[
        create_gcs_bucket,
        upload_file_to_bucket,
    ],
)
