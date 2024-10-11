from fastapi import APIRouter, status
from fastapi.params import Depends
from openai import OpenAI

from backend.schemas import ExceptionSchema
from backend.schemas.chat import (
    DocSummarizationResponse,
    DocSummarizationRequest,
    QuestionAnswerResponse,
    QuestionAnswerRequest,
    CreateChatRequest, ChatIdResponse, ChatFileContentResponse, ChatSessionResponse,
)
from backend.services.auth_bearer import get_current_user_id
from backend.services.chat import create_chat_session, create_chat_history, get_file_contents_from_fs, \
    get_chat_session_obj
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
    return await create_chat_history(chat_id, request.question, openai_client, request.model)


@docs_router.get(
    "/{chat_id}/file-content",
    response_model=ChatFileContentResponse
)
async def get_file_content(chat_id: int, user_id: int = Depends(get_current_user_id)) -> ChatFileContentResponse:
    file_contents = await get_file_contents_from_fs(chat_id)
    return ChatFileContentResponse(file_contents=file_contents)


@docs_router.get(
    "/{chat_id}/",
    response_model=ChatSessionResponse
)
async def get_file_content(chat_id: int, user_id: int = Depends(get_current_user_id)) -> ChatSessionResponse:
    return await get_chat_session_obj(chat_id)
