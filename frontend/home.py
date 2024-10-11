import streamlit as st

def main():
    st.title("PDF QUESTION ANSWERING APP")

    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.7); padding: 20px; border-radius: 10px;">
        <h2 style="color: #1e3d59;">Welcome to the PDF QUESTION ANSWERING APP</h2>
        <p>This tool allows you to:</p>
        <ul>
            <li>This app uses appache airflow to show manage Text extraction which done using Pypdf and AWSTextExtract</li>
            <li>User can ask question to PDF</li>
            <li>Based on the extracted text user for the selected pdf file</li>
            <li>User has to select the openai model</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.7); padding: 20px; border-radius: 10px; margin-top: 20px;">
        <h3 style="color: #1e3d59;">Getting Started</h3>
        <p>Use the navigation sidebar to explore different functionalities:</p>
        <ol>
            <li>Register a new user</li>
            <li>Login with the registered user</li>
             <li>After Login authentication user can access a pdf questioning page</li>
            <li>User has to select a pdf required for their use</li>
            <li>User has to select the text extraction method</li>
            <li>User has to select the openai model</li>
            <li>Ask question in the text window for their Use case</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
