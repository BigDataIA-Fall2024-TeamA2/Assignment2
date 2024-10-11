import logging

from openai import OpenAI, OpenAIError

from backend.database.chat_session import create_db_chat_session, get_chat_session
from backend.database.pdf_extractions import fetch_all_pdf_extractions, get_a_specific_pdf, PdfExtractionsModel
from backend.schemas.chat import SingleDocModel, CompleteSingleDocResponse, ChatIdResponse

logger = logging.getLogger(__name__)


async def _invoke_openai_api(openai_client: OpenAI, model: str, user_prompt: str):
    try:
        completion = openai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an assistant designed to provide clear and accurate answers based on the information in the user's prompt. Use your knowledge to reason through the query and offer concise, relevant, and well-explained responses.""",
                },
                {"role": "user", "content": user_prompt},
            ],
        )
    except OpenAIError as e:
        err_msg = e.body["message"]
        logger.error(f"Error while invoking OpenAI API with model: {model} | Error: {err_msg}")
        return f"Error invoking OpenAI API: {err_msg}"
    return completion.choices[0].message.content


async def list_all_pdfs():
    pdf_list = fetch_all_pdf_extractions()
    return [SingleDocModel(id=pdf[0], filename=pdf[1], extraction_mechanism=pdf[2]) for pdf in pdf_list]


async def get_specific_pdf(filename: str, extraction_mechanism: str) -> CompleteSingleDocResponse | None:
    filtered_results = get_a_specific_pdf(filename, extraction_mechanism)
    if len(filtered_results) > 0:
        pdf_extraction = filtered_results[0]
        return CompleteSingleDocResponse(
            id=pdf_extraction.id,
            filename=pdf_extraction.filename,
            s3_bucket=pdf_extraction.s3_bucket,
            source_file_key=pdf_extraction.source_file_key,
            extracted_file_key=pdf_extraction.extracted_file_key,
            extracted_media_key=pdf_extraction.extracted_media_key,
            extraction_status=pdf_extraction.extraction_status,
            extraction_mechanism=pdf_extraction.extraction_mechanism,
        )
    return None


async def create_chat_session(filename, extraction_mechanism, user_id) -> ChatIdResponse | None:
    file_obj = await get_specific_pdf(filename, extraction_mechanism)


    if file_obj is not None:
        new_chat_session = create_db_chat_session(user_id, file_obj.id)
        return ChatIdResponse(chat_id=new_chat_session.chat_id)
    return None


async def create_chat_history(chat_id: int, question: str):
    chat_session_obj = get_chat_session(chat_id)
    ...