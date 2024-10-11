from fastapi import APIRouter, status
from fastapi.params import Depends
from openai import OpenAI

from backend.database.pdf_extractions import fetch_all_pdf_extractions
from backend.schemas import ExceptionSchema
from backend.schemas.chat import (
    DocSummarizationResponse,
    DocSummarizationRequest,
    QuestionAnswerResponse,
    QuestionAnswerRequest,
    DocsListResponse,
    CreateChatRequest, ChatIdResponse,
)
from backend.services.auth_bearer import JWTBearer, get_current_user_id
from backend.services.chat import list_all_pdfs, create_chat_session
from backend.utils import get_openai_client
from backend.views.choices import security_scheme

docs_router = APIRouter(prefix="/chat", tags=["chat"])

@docs_router.post(
    "/summarization",
    response_model=DocSummarizationResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema}},
)
async def summarize_document(
    request: DocSummarizationRequest,
    openai_client: OpenAI = Depends(get_openai_client),
    token: str = Depends(security_scheme),
) -> DocSummarizationResponse:
    return await ...


@docs_router.post("/initiate", response_model=ChatIdResponse)
async def create_chat(request: CreateChatRequest, user_id: int = Depends(get_current_user_id)) -> ChatIdResponse:
    return await create_chat_session(request.filename, request.extraction_mechanism, user_id)


@docs_router.post(
    "/{chat_id}/qa",
    response_model=QuestionAnswerResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema}},
)
async def question_answer(
    chat_id: int,
    request: QuestionAnswerRequest,
    openai_client: OpenAI = Depends(get_openai_client),
    user_id: int = Depends(get_current_user_id)
) -> QuestionAnswerResponse:
    return await ...


# @docs_router.get("/", response_model=DocsListResponse)
# async def fetch_all_documents(token: str = Depends(security_scheme)) -> DocsListResponse:
#     docs_list = await list_all_pdfs()
#     return DocsListResponse(docs=docs_list)


@docs_router.get(
    "/file-content",
    response_model=""
)
async def get_file_content(filename: str, extraction_mechanism: str):
    ...

