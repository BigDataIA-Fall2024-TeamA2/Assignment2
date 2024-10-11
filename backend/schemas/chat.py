from pydantic import BaseModel


class DocSummarizationRequest(BaseModel):
    doc_content: str


class DocSummarizationResponse(BaseModel):
    summarized_doc: str


class QuestionAnswerRequest(BaseModel):
    question: str
    model: str

class QuestionAnswerResponse(BaseModel):
    llm_response: str


class SingleDocModel(BaseModel):
    id: int
    filename: str
    extraction_mechanism: str


class DocsListResponse(BaseModel):
    docs: list[SingleDocModel]


class CreateChatRequest(BaseModel):
    openai_model: str
    filename: str
    extraction_mechanism: str

class ChatIdResponse(BaseModel):
    chat_id: int


class ChatSessionResponse(BaseModel):
    chat_id: int
    filename: str


class CompleteSingleDocResponse(SingleDocModel):
    id: int 
    filename: str
    s3_bucket: str
    source_file_key: str
    extracted_file_key: str
    extracted_media_key: str | None
    extraction_status: str
    extraction_mechanism: str

class ChatFileContentResponse(BaseModel):
    file_contents: str


