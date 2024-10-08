from pydantic import BaseModel


class DocSummarizationRequest(BaseModel):
    doc_content: str


class DocSummarizationResponse(BaseModel):
    summarized_doc: str


class QuestionAnswerRequest(BaseModel):
    question: str
    doc_content: str
    model: str


class QuestionAnswerResponse(BaseModel):
    llm_response: str
