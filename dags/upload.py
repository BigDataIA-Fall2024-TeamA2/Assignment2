import boto3
import os
from botocore.exceptions import NoCredentialsError

def upload_files_to_s3(local_dir, bucket_name, s3_prefix=''):
    """
    Upload all files from a local directory to an S3 bucket.
    
    :param local_dir: Local directory containing files to upload
    :param bucket_name: Name of the S3 bucket
    :param s3_prefix: Prefix to add to S3 object keys (optional)
    """
    s3_client = boto3.client('s3')
    
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_dir)
            s3_path = os.path.join(s3_prefix, relative_path).replace("\\", "/")
            
            try:
                print(f"Uploading {local_path} to {bucket_name}/{s3_path}")
                s3_client.upload_file(local_path, bucket_name, s3_path)
                print(f"Successfully uploaded {file}")
            except FileNotFoundError:
                print(f"File not found: {local_path}")
            except NoCredentialsError:
                print("Credentials not available")
                return False
            except Exception as e:
                print(f"Error uploading {file}: {str(e)}")
    
    return True

def main_uploader():
    bucket_name = "damg7374-a2-store"
    
    # Define the directories and their corresponding S3 prefixes
    directories = [
        {
            "local_path": "/tmp/resources/file_attachments",
            "s3_prefix": "gaia-pdfs"
        },
        {
            "local_path": "/tmp/resources/extracted_text",
            "s3_prefix": "extracted-text"
        }
    ]
    
    for directory in directories:
        local_directory = directory["local_path"]
        s3_prefix = directory["s3_prefix"]
        
        if not os.path.exists(local_directory):
            print(f"Error: Directory {local_directory} does not exist.")
            continue
        
        print(f"Starting upload from {local_directory} to S3 bucket {bucket_name}/{s3_prefix}")
        
        success = upload_files_to_s3(local_directory, bucket_name, s3_prefix)
        
        if success:
            print(f"All files from {local_directory} uploaded successfully")
        else:
            print(f"There was an issue uploading files from {local_directory}")

    print("Upload process completed.")

if __name__ == "__main__":
    main_uploader()