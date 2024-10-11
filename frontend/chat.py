import streamlit as st
import requests
from backend.schemas.docs import DocsListResponse, DocSummarizationRequest, DocSummarizationResponse, QuestionAnswerRequest, QuestionAnswerResponse
from frontend.login import get_auth_token, refresh_auth_token

BASE_URL = "http://localhost:8000"

def get_pdf_files(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/docs/", headers=headers)
    if response.status_code == 200:
        docs_list_response = DocsListResponse(**response.json())
        return [doc.filename for doc in docs_list_response.docs]
    else:
        st.error("Failed to fetch PDF files")
        return []

def summarize_pdf(pdf_name, extraction_mechanism, token):
    headers = {"Authorization": f"Bearer {token}"}
    data = DocSummarizationRequest(doc_content=pdf_name).dict()
    response = requests.post(f"{BASE_URL}/docs/summarization", json=data, headers=headers)
    if response.status_code == 200:
        summarization_response = DocSummarizationResponse(**response.json())
        return summarization_response.summarized_doc
    else:
        st.error(f"Failed to summarize PDF: {response.status_code} - {response.text}")
        return "Error: Unable to summarize PDF"

def get_answer(pdf_name, question, model, token):
    headers = {"Authorization": f"Bearer {token}"}
    data = QuestionAnswerRequest(question=question, doc_content=pdf_name, model=model).dict()
    response = requests.post(f"{BASE_URL}/docs/qa", json=data, headers=headers)
    if response.status_code == 200:
        qa_response = QuestionAnswerResponse(**response.json())
        return qa_response.llm_response
    else:
        st.error(f"Failed to get answer: {response.status_code} - {response.text}")
        return "Error: Unable to get answer"

def main():
    st.title("PDF Question Answering App")

    # Check if user is logged in
    if "access_token" in st.session_state:
        token = st.session_state["access_token"]

        # Sidebar for PDF selection
        st.header("PDF Selection")
        pdf_files = get_pdf_files(token)
        selected_pdf = st.selectbox("Choose a PDF", pdf_files)

        # Selectbox for model selection
        model_options = ["gpt-4o-2024-05-13", "gpt-4o-mini-2024-07-18"]
        selected_model = st.selectbox("Select a Model", model_options, key="model_select")

        # Selectbox for extraction mechanism
        extraction_methods = ["PyPDF2", "AWS Textract"]
        selected_method = st.selectbox("Select Extraction Method", extraction_methods, key="extraction_method")

        # Main area for content and user input
        if selected_pdf:
            st.write(f"Selected PDF: **{selected_pdf}**")

            # Get PDF summary
            summary = summarize_pdf(selected_pdf, selected_method, token)

            # Display a preview of the PDF summary
            st.subheader("PDF Summary")
            st.text_area("Summary", summary[:500] + "...", height=150, disabled=True)

            # User input text area
            st.subheader("Ask a Question")
            user_question = st.text_area("Enter your question about the PDF:", height=100)

            if st.button("Get Answer"):
                if user_question:
                    # Call QA endpoint
                    with st.spinner("Generating answer..."):
                        answer = get_answer(selected_pdf, user_question, selected_model, token)

                    st.subheader("Answer:")
                    st.write(answer)
                else:
                    st.warning("Please enter a question.")
        else:
            st.info("Please select a PDF file from the sidebar.")
    else:
        st.info("Please log in to access the app.")

if __name__ == "__main__":
    main()
