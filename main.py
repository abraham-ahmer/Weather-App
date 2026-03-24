from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database_models import Base
from database import engine
from authentication import login, signup
import weather
from fastapi.exceptions import RequestValidationError

app = FastAPI(title="Weather App")

Base.metadata.create_all(bind=engine)


@app.exception_handler(RequestValidationError)
async def email_error_handler(request:Request, exc:RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=["Invalid email. Please enter a valid email for signup"]
    )



app.include_router(login.router)
app.include_router(signup.router)
app.include_router(weather.router)


@app.get("/")
def greet():
    return {"message":"Check weather G"}







