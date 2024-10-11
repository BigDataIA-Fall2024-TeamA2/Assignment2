import logging

from openai import OpenAI, OpenAIError

from backend.database.pdf_extractions import fetch_all_pdf_extractions
from backend.schemas.chat import SingleDocModel

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
