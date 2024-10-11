import os
import requests
from bs4 import BeautifulSoup
import time

def get_pdf_file_links(url):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                print(f"Failed to access {url} after {max_retries} attempts")
                return []
            time.sleep(2)  # Wait before retrying

    print(f"Getting links from {url}")
    soup = BeautifulSoup(response.text, "html.parser")
    file_links = [link.get("href").split("/")[-1] for link in soup.find_all("a") 
                  if link.get("href") and link.get("href").endswith('.pdf')]
    return file_links

def download_file(file_url, file_path):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(file_url, timeout=10)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {file_path} successfully.")
            return True
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed to download {file_url}: {e}")
            if attempt == max_retries - 1:
                print(f"Failed to download {file_url} after {max_retries} attempts")
            else:
                time.sleep(2)  # Wait before retrying
    return False

def download_files(file_links, raw_base_url, download_dir):
    if not file_links:
        print("No PDF files found to download.")
        return

    for file_name in file_links:
        file_url = f"{raw_base_url}{file_name}"
        file_path = os.path.join(download_dir, file_name)
        print(f"Attempting to download {file_url}...")
        download_file(file_url, file_path)

def pdf_downloader_main():
    github_base = "https://github.com/aymeric-roucher/GAIA"
    test_base_url = f"{github_base}/tree/main/data/gaia/test"
    validation_base_url = f"{github_base}/tree/main/data/gaia/validation"
    raw_github_base = "https://raw.githubusercontent.com/aymeric-roucher/GAIA/main/data/gaia"

    download_dir = "/tmp/resources/file_attachments"
    os.makedirs(download_dir, exist_ok=True)

    print(f"Download directory: {download_dir}")

    # Get and download test files
    test_pdf_links = get_pdf_file_links(test_base_url)
    print(f"Found {len(test_pdf_links)} test PDF links")
    download_files(test_pdf_links, f"{raw_github_base}/test/", download_dir)

    # Get and download validation files
    validation_pdf_links = get_pdf_file_links(validation_base_url)
    print(f"Found {len(validation_pdf_links)} validation PDF links")
    download_files(validation_pdf_links, f"{raw_github_base}/validation/", download_dir)

    print("Download process completed.")

if __name__ == "__main__":
    pdf_downloader_main()