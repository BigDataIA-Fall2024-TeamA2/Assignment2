from functools import lru_cache

import streamlit as st

from frontend.utils.chat import get_openai_model_choices, get_extraction_mechanism_choices, get_unique_pdf_filenames, \
    get_pdf_object_from_db


def qa_interface():
    st.title("Question Answering Interface")

    openai_models_choice = st.selectbox("Choose an OpenAI model", get_openai_model_choices())
    extraction_mechanism_choice = st.selectbox("Choose a PDF extraction method", get_extraction_mechanism_choices())
    pdf_file_choice = st.selectbox("Choose a PDF file", get_unique_pdf_filenames())

    if pdf_file_choice:
        pdf_file_obj = get_pdf_object_from_db(pdf_file_choice, extraction_mechanism_choice)

    if all([openai_models_choice, extraction_mechanism_choice, pdf_file_choice]):
        ...
