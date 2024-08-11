import boto3
from google.cloud import storage
from azure.storage.blob import BlobServiceClient


class CloudStorageService:
    def __init__(self, provider, **credentials):
        self.provider = provider
        if provider == "aws":
            self.client = boto3.client("s3", **credentials)
        elif provider == "gcp":
            self.client = storage.Client(**credentials)
        elif provider == "azure":
            self.client = BlobServiceClient(**credentials)
        else:
            raise ValueError("Unsupported cloud storage provider")

    def upload_file(self, bucket_name, file_path, object_name=None):
        if self.provider == "aws":
            return self._upload_to_s3(bucket_name, file_path, object_name)
        elif self.provider == "gcp":
            return self._upload_to_gcp(bucket_name, file_path, object_name)
        elif self.provider == "azure":
            return self._upload_to_azure(bucket_name, file_path, object_name)

    def _upload_to_s3(self, bucket_name, file_path, object_name=None):
        object_name = object_name or file_path
        self.client.upload_file(file_path, bucket_name, object_name)
        return f"File uploaded to S3: {bucket_name}/{object_name}"

    def _upload_to_gcp(self, bucket_name, file_path, object_name=None):
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(object_name or file_path)
        blob.upload_from_filename(file_path)
        return f"File uploaded to GCP: {bucket_name}/{object_name or file_path}"

    def _upload_to_azure(self, bucket_name, file_path, object_name=None):
        container_client = self.client.get_container_client(bucket_name)
        with open(file_path, "rb") as data:
            container_client.upload_blob(name=object_name or file_path, data=data)
        return f"File uploaded to Azure Blob Storage: {bucket_name}/{object_name or file_path}"
