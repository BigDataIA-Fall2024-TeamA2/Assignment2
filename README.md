# Question Answering Interface

## Application Summary:

This application is a Retrieval-Augmented Generation (RAG)-based system where users can interact with an LLM to ask questions about the content of uploaded documents. It consists of two main components: a Streamlit frontend and a FastAPI backend.

Links to Resources:
1. [CodeLabs Link](https://codelabs-preview.appspot.com/?file_id=1WFuc5ShwnSdNSBE-l3amYXxE4B6U5xpitCTYttudxMI#0)
2. [Deployed Streamlit Frontend](http://98.81.209.60:8501/)
3. [Deployed FastAPI Backend](http://98.81.209.60:8000/docs/)
4. [Demo Video](video/video.mov)
  

## Frontend (Streamlit):

The frontend provides a simple interface with three pages:

    User Creation: Allows new users to register by creating an account.
    Login: Authenticates users via JWT-based token authentication.
    Question Answering Interface:
        Users can select an LLM model, extraction method, and upload a document.
        The document content is displayed, and users can ask questions related to the file.
        The frontend sends these inputs to the backend to retrieve an answer.

## Backend (FastAPI):

The backend handles core functionalities:

    User Management: Supports user registration and JWT-based login.
    Question Answering Service:
        Uses extracted file content from Airflow workflows.
        Allows users to select different LLM models to generate answers based on the extracted content.

All relevant requests are authenticated to ensure secure interactions.

## Attestation

WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

Contribution:

    a. Gopi Krishna Gorle: 33%
    b. Pranali Chipkar: 33%
    c. Mubin Modi: 33%

## Installation
1. Clone the repository
  ```bash
    git clone https://github.com/BigDataIA-Fall2024-TeamA2/Assignment2 && cd Assignment2
  ```
2. Setup local environment by creating a virtual environment and the `.env` file (For *unix systems)
```bash
python3 -m venv venv
./venv/bin/activate.sh
 pip install -r reqirements.txt
 cp .env.template .env
```
4. Fill in the relevant secrets in `.env` file.
5. The application is dockerized and doesn't depend on external dependencies. Using the following command the frontend, backend applications can be started:
```bash
docker compose up -d
```

## Usage Instructions
1. The streamlit frontend, allows the unauthenticated users to either create a new account or login to existing accounts
2. Once logged in (after creating an account), the user has the two options. Either to use the question answering interface or logout from his existing account.


## Repository Overview
```bash
.
├── README.md
├── app.py
├── architecture
│   ├── Airflow_pipeline.drawio
│   ├── Airflow_pipeline.png
│   ├── StreamlitApp.drawio
│   └── StreamlitApp.png
├── backend
│   ├── __init__.py
│   ├── config.py
│   ├── database
│   │   ├── __init__.py
│   │   ├── chat_history.py
│   │   ├── chat_session.py
│   │   ├── pdf_extractions.py
│   │   └── users.py
│   ├── logging.conf
│   ├── main.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── choices.py
│   │   └── users.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── auth_bearer.py
│   │   ├── chat.py
│   │   └── users.py
│   ├── utils.py
│   └── views
│       ├── __init__.py
│       ├── auth.py
│       ├── chat.py
│       ├── choices.py
│       └── users.py
├── backend.Dockerfile
├── dags
│   ├── db.py
│   ├── extract.py
│   ├── pdf_downloader.py
│   ├── pdf_extractions.py
│   ├── pipeline.py
│   └── upload_downloaded_pdfs.py
├── docker-compose-airflow.yaml
├── docker-compose-app.yaml
├── frontend
│   ├── __init__.py
│   ├── config.py
│   ├── pages
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── user_creation.py
│   │   └── user_login.py
│   └── utils
│       ├── __init__.py
│       ├── auth.py
│       └── chat.py
├── frontend.Dockerfile
├── pyproject.toml
├── requirements.txt
└── video
    └── video.mov

```
