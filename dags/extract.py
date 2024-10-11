

import boto3
import time
from botocore.exceptions import NoCredentialsError, ClientError, ParamValidationError
from io import BytesIO
from PyPDF2 import PdfReader
from pdf_extractions import create_pdf_extraction
 # Import the existing database function

def extract_text_using_textract_async(file_key, bucket_name):
    aws_region = boto3.Session().region_name or 'us-east-1'
    
    try:
        textract = boto3.client('textract', region_name=aws_region)
        s3 = boto3.client('s3', region_name=aws_region)
        
        # Check file size
        response = s3.head_object(Bucket=bucket_name, Key=file_key)
        file_size = response['ContentLength']
        
        print(f"File size: {file_size} bytes")
        
        if file_size > 500 * 1024 * 1024:  # 500 MB limit
            print(f"File too large for Textract: {file_key}")
            return None
        
        # Start an asynchronous job for text detection
        response = textract.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': file_key
                }
            }
        )
        
        job_id = response['JobId']
        print(f"Started Textract job with ID: {job_id}")
        
        # Wait for the job to complete
        while True:
            response = textract.get_document_text_detection(JobId=job_id)
            status = response['JobStatus']
            print(f"Job status: {status}")
            
            if status in ['SUCCEEDED', 'FAILED']:
                break
            
            time.sleep(5)  # Wait for 5 seconds before checking again
        
        if status == 'SUCCEEDED':
            # Extract text from the job results
            text = ""
            
            # Process initial response
            for item in response['Blocks']:
                if item['BlockType'] == 'LINE':
                    text += item['Text'] + "\n"
            
            # Handle pagination if the response is truncated
            while 'NextToken' in response:
                response = textract.get_document_text_detection(
                    JobId=job_id,
                    NextToken=response['NextToken']
                )
                
                for item in response['Blocks']:
                    if item['BlockType'] == 'LINE':
                        text += item['Text'] + "\n"
            
            return text
        else:
            print(f"Textract job failed for {file_key}")
            return None
        
    except Exception as e:
        print(f"Error extracting text using Textract from {file_key}: {e}")
    
    return None

def extract_text_using_pypdf(file_key, bucket_name):
    s3 = boto3.client('s3')
    
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read()
        
        pdf_file = PdfReader(BytesIO(file_content))
        text = ""
        
        for page in pdf_file.pages:
            text += page.extract_text() + "\n"
        
        return text
    except Exception as e:
        print(f"Error extracting text using PyPDF2 from {file_key}: {e}")
    
    return None

def process_s3_pdfs(bucket_name, folder_name):
    s3 = boto3.client('s3')
    
    try:
        # List all objects in the specified S3 bucket and folder
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
        
        if 'Contents' not in response:
            print(f"No files found in s3://{bucket_name}/{folder_name}")
            return

        for obj in response['Contents']:
            file_key = obj['Key']
            filename = file_key.split('/')[-1]
            
            if not filename.lower().endswith('.pdf'):
                continue
            
            print(f"Processing file: s3://{bucket_name}/{file_key}")
            
            # Extract text using AWS Textract
            textract_text = extract_text_using_textract_async(file_key, bucket_name)
            
            if textract_text:
                output_key = f"extracted_text/{filename.rsplit('.', 1)[0]}_textract.txt"
                s3.put_object(Bucket=bucket_name, Key=output_key, Body=textract_text.encode('utf-8'))
                print(f"Saved Textract extracted text to s3://{bucket_name}/{output_key}")
                
                # Store Textract extraction in database
                create_pdf_extraction(
                    filename=filename,
                    s3_bucket=bucket_name,
                    source_file_key=file_key,
                    extracted_file_key=output_key,
                    extracted_media_key=None,
                    extraction_status="COMPLETED",
                    extraction_mechanism="Textract"
                )
            else:
                print(f"Failed to extract text using AWS Textract for {file_key}")
                create_pdf_extraction(
                    filename=filename,
                    s3_bucket=bucket_name,
                    s3_key=file_key,
                    source_file_key=file_key,
                    extracted_file_key=None,
                    extracted_media_key=None,
                    extraction_status="FAILED",
                    extraction_mechanism="Textract"
                )
            
            # Extract text using PyPDF2
            pypdf_text = extract_text_using_pypdf(file_key, bucket_name)
            
            if pypdf_text:
                output_key = f"extracted_text/{filename.rsplit('.', 1)[0]}_pypdf.txt"
                s3.put_object(Bucket=bucket_name, Key=output_key, Body=pypdf_text.encode('utf-8'))
                print(f"Saved PyPDF2 extracted text to s3://{bucket_name}/{output_key}")
                
                # Store PyPDF2 extraction in database
                create_pdf_extraction(
                    filename=filename,
                    s3_bucket=bucket_name,
                    source_file_key=file_key,
                    extracted_file_key=output_key,
                    extracted_media_key=None,
                    extraction_status="COMPLETED",
                    extraction_mechanism="PyPDF"
                )
            else:
                print(f"Failed to extract text using PyPDF2 for {file_key}")
                create_pdf_extraction(
                    filename=filename,
                    s3_bucket=bucket_name,
                    source_file_key=file_key,
                    extracted_file_key=None,
                    extracted_media_key=None,
                    extraction_status="FAILED",
                    extraction_mechanism="PyPDF"
                )
        
    except Exception as e:
        print(f"Error processing S3 PDFs: {e}")

# Main workflow
def process_pdfs():
    bucket_name = "damg7374-a2-store"
    folder_name = "gaia-pdfs/"
    process_s3_pdfs(bucket_name, folder_name)

# Run the script
if __name__ == "__main__":
    process_pdfs()