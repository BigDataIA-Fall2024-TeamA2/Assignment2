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
    ChatResponse,
    CreateChatRequest,
)
from backend.services.auth_bearer import JWTBearer
from backend.services.chat import list_all_pdfs
from backend.utils import get_openai_client

docs_router = APIRouter(prefix="/chat", tags=["chat"])

security_scheme = JWTBearer()


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


@docs_router.post("/initialize", response_model=ChatResponse)
async def create_chat(request: CreateChatRequest, token: str = Depends(security_scheme)): ...


@docs_router.post(
    "/{chat_id}/qa",
    response_model=QuestionAnswerResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema}},
)
async def question_answer(
    chat_id: str,
    request: QuestionAnswerRequest,
    openai_client: OpenAI = Depends(get_openai_client),
    token: str = Depends(security_scheme),
) -> QuestionAnswerResponse:
    return await ...


@docs_router.get("/", response_model=DocsListResponse)
async def fetch_all_documents(token: str = Depends(security_scheme)) -> DocsListResponse:
    docs_list = await list_all_pdfs()
    return DocsListResponse(docs=docs_list)
