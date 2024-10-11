from fastapi import APIRouter, Depends

from backend.schemas.chat import DocsListResponse, CompleteSingleDocResponse
from backend.schemas.choices import ChoicesResponse
from backend.services.auth_bearer import JWTBearer
from backend.services.chat import list_all_pdfs, get_specific_pdf

choices_router = APIRouter(prefix="/choices", tags=["choices"])
security_scheme = JWTBearer()


@choices_router.get("/openai-models", response_model=ChoicesResponse)
async def get_openai_model_choices() -> ChoicesResponse:
    """
    Returns a list of available OpenAI model choices.
    """
    supported_openai_models = ["gpt-4o-2024-05-13", "gpt-4o-mini-2024-07-18"]
    return ChoicesResponse(choices=supported_openai_models)


@choices_router.get("/pdf-extraction-mechanisms", response_model=ChoicesResponse)
async def get_pdf_extraction_mechanism_choices() -> ChoicesResponse:
    """
    Returns a list of available PDF extraction mechanism choices.
    """
    # Assuming you have a list or dictionary of PDF extraction mechanisms
    pdf_extraction_mechanisms = ["PyPDF", "Textract"]
    return ChoicesResponse(choices=pdf_extraction_mechanisms)



@choices_router.get("/pdfs", response_model=DocsListResponse)
async def get_pdf_files(token: str = Depends(security_scheme)) -> DocsListResponse:
    """
    Returns a list of available PDF files.
    """
    docs_list = await list_all_pdfs()
    return DocsListResponse(docs=docs_list)


@choices_router.get("/pdf/", response_model=CompleteSingleDocResponse)
async def get_pdf_file(filename: str, extraction_mechanism: str, token: str = Depends(security_scheme)) -> CompleteSingleDocResponse:
    return await get_specific_pdf(filename, extraction_mechanism)
