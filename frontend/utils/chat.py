from functools import lru_cache
import streamlit as st

from frontend.utils.auth import make_authenticated_request, make_unauthenticated_request


@lru_cache
def get_openai_model_choices():
    return make_unauthenticated_request(
        endpoint="/choices/openai-models",
        method="GET"
    )["choices"]


@lru_cache
def get_extraction_mechanism_choices():
    return make_unauthenticated_request(
        endpoint="/choices/pdf-extraction-mechanisms",
        method="GET"
    )["choices"]


@lru_cache
def _get_pdf_files_list():
    return make_authenticated_request(
        endpoint="/choices/pdfs",
        method="GET"
    )


def get_unique_pdf_filenames():
    return set(pdf["filename"] for pdf in _get_pdf_files_list()["docs"])


def get_pdf_object_from_db(pdf_filename: str, extraction_mechanism: str):
    return make_authenticated_request(
        endpoint="/choices/pdf",
        method="GET",
        params={"filename": pdf_filename, "extraction-mechanism": extraction_mechanism}
    )


def get_pdf_file_from_s3(s3_bucket: str, file_key: str):
    ...


def set_chat_id(chat_id: str):
    st.session_state.chat_id = chat_id


def get_chat_id():
    if hasattr(st.session_state, "chat_id") and st.session_state.chat_id is not None:
        return st.session_state.chat_id
    raise ValueError("chat_id not set")


def revoke_chat_id():
    st.session_state.chat_id = None


def initiate_chat():
    response = make_authenticated_request(
        endpoint="/chat/initiate",

    )


def ask_question(question: str, model: str, filename_id: str):
    return make_authenticated_request(
        endpoint=""
    )