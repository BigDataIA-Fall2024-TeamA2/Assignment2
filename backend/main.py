from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import users, auth

app = FastAPI()

app.add_middleware(CORSCorsMiddleware)
app.include_router(users.router)
app.include_router(auth.router)
