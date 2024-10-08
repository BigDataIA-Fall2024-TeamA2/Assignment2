
from fastapi import APIRouter, status
from fastapi.params import Depends
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import db_session
from backend.schemas.docs import DocSummarizationResponse, DocSummarizationRequest, QuestionAnswerResponse, \
    QuestionAnswerRequest
from backend.utils import get_openai_client

docs_router = APIRouter(prefix="/docs")

@docs_router.post("/summarization",
                  response_model=DocSummarizationResponse,
                  responses={status.HTTP_401_UNAUTHORIZED: {"model": Exception}},
                )
async def summarize_document(request: DocSummarizationRequest, db: AsyncSession = Depends(db_session),
                             openai_client: OpenAI = Depends(get_openai_client)) -> DocSummarizationResponse:
    return await ...


@docs_router.post("/qa",
                  response_model=QuestionAnswerResponse,
                  responses={status.HTTP_401_UNAUTHORIZED: {"model": Exception}},
                )
async def summarize_document(request: QuestionAnswerRequest, db: AsyncSession = Depends(db_session),
                             openai_client: OpenAI = Depends(get_openai_client)) -> QuestionAnswerResponse:
    return await ...


