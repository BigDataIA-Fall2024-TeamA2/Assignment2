import streamlit as st
import os
import asyncio
from backend.services.chat import _invoke_openai_api
import PyPDF2
from backend.utils import get_openai_client
def get_pdf_files():
    """
    Function to get PDF files from a specific directory.
    """
    pdf_directory = "D:\Projects\Assignment2"  # Replace with your actual PDF directory path
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    return pdf_files


def load_pdf_content(pdf_name):
    """
    Function to load PDF content using PyPDF2.
    """
    pdf_directory = "D:\Projects\Assignment2"  # Replace with your actual PDF directory path
    pdf_path = os.path.join(pdf_directory, pdf_name)

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() if page.extract_text() else ''
    return text


def main():
    st.title("PDF Question Answering App")

    # Sidebar for PDF selection
    st.sidebar.header("PDF Selection")
    pdf_files = get_pdf_files()
    selected_pdf = st.sidebar.selectbox("Choose a PDF", pdf_files)

    # Selectbox for model selection
    model_options = ["gpt-4o-2024-05-13", "gpt-4o-mini-2024-07-18"]
    selected_model = st.selectbox("Select a Model", model_options, key="model_select")

    # Main area for content and user input
    if selected_pdf:
        st.write(f"Selected PDF: **{selected_pdf}**")

        # Load PDF content
        pdf_content = load_pdf_content(selected_pdf)

        # Display a preview of the PDF content
        st.subheader("PDF Content Preview")
        st.text_area("PDF Content", pdf_content[:500] + "...", height=150, disabled=True)

        # User input text area
        st.subheader("Ask a Question")
        user_question = st.text_area("Enter your question about the PDF:", height=100)

        if st.button("Get Answer"):
            if user_question:
                # Combine PDF content and user question
                prompt = f"PDF Content: {pdf_content}\n\nUser Question: {user_question}"

                # Call OpenAI API
                with st.spinner("Generating answer..."):
                    answer = asyncio.run(
                        _invoke_openai_api(get_openai_client, user_prompt=prompt, model=selected_model))

                st.subheader("Answer:")
                st.write(answer)
            else:
                st.warning("Please enter a question.")
    else:
        st.info("Please select a PDF file from the sidebar.")


if __name__ == "__main__":
    main()
