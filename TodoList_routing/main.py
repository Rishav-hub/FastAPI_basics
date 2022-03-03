from typing import Optional
from fastapi import FastAPI, Depends
import models
from database import engine
from sqlalchemy.orm import Session
from company import companyapi, dependencies
from routers import auth, todos


app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(
        companyapi.router, 
        prefix="/company",
        tags=["company"],
        dependencies=[Depends(dependencies.get_token_header)],
        responses={"418": {"description": "Internal use only"}})


