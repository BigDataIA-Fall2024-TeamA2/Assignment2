# dags/gaia_text_extraction.py

from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from extract import process_pdfs
from pdf_downloader import pdf_downloader_main
from upload import main_uploader

# Base URLs and download directory
download_dir = "/tmp/resources/file_attachments"

default_args = {
    "owner": "airflow",
    "start_date": datetime.now(),
    "retries": 1,
}

with DAG("gaia_text_extraction", default_args=default_args) as dag:

    download_task = PythonOperator(
        task_id="download_pdfs",
        python_callable=pdf_downloader_main,
        dag=dag,
    )

    process_task = PythonOperator(
        task_id="process_pdfs",
        python_callable=process_pdfs,
        op_kwargs={
            "pdf_directory": download_dir,
        },
        dag=dag,
    )

    upload_task = PythonOperator(
        task_id="upload_pdfs",
        python_callable=main_uploader,
        dag=dag,
    )

    download_task >> process_task >> upload_task  # Set task dependencies
