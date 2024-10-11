import os

import PyPDF2
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from backend.database.pdf_extractions import create_pdf_extraction

# Directory containing PDFs
pdf_directory = "/tmp/resources/file_attachments/"
# Directory to save extracted text files

# Create output directory if it doesn't exist


# Function to extract text using PyPDF2
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path} using PyPDF2: {e}")
        return None


# Function to extract text using AWS Textract (local file processing for image-based PDFs)
def extract_text_using_textract_local(pdf_path):
    aws_region = os.environ["AWS_DEFAULT_REGION"]

    try:
        textract = boto3.client("textract", region_name=aws_region)

        with open(pdf_path, "rb") as file:
            response = textract.detect_document_text(Document={"Bytes": file.read()})

        blocks = response.get("Blocks", [])
        text = ""
        for block in blocks:
            if block["BlockType"] == "LINE":
                text += block["Text"] + "\n"
        create_pdf_extraction(...)
        return text
    except NoCredentialsError as e:
        print(e)
        print("Error: AWS credentials not found.")
        return None
    except ClientError as e:
        print(f"AWS Textract client error: {e}")
        return None
    except Exception as e:
        print(f"Error extracting text from {pdf_path} using AWS Textract: {e}")
        return None


# Function to save extracted text to a file
def save_text_to_file(output_directory, text, filename, method):
    if text:
        output_filename = f"{os.path.splitext(filename)[0]}_{method}.txt"
        output_path = os.path.join(output_directory, output_filename)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Saved extracted text to {output_path}")
    else:
        print(f"No text to save for {filename} using {method}")


# Main workflow
def process_pdfs(pdf_directory):
    output_directory = "/tmp/resources/extracted_text/"
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)

            # Extract text using PyPDF2
            pypdf2_text = extract_text_from_pdf(pdf_path)
            print(f"\nExtracted text from {filename} using PyPDF2:")
            print("-" * 50)
            if pypdf2_text:
                save_text_to_file(output_directory, pypdf2_text, filename, "pypdf2")
            else:
                print("Failed to extract text using PyPDF2.")

            print("\n" + "=" * 50)

            # Extract text using AWS Textract
            textract_text = extract_text_using_textract_local(pdf_path)
            print(f"\nExtracted text from {filename} using AWS Textract:")
            print("-" * 50)
            if textract_text:
                save_text_to_file(output_directory, textract_text, filename, "textract")
            else:
                print("Failed to extract text using AWS Textract.")

    print("List of files in extracted folder")
    print(os.listdir(output_directory))


# Run the script
if __name__ == "__main__":
    process_pdfs(pdf_directory)
