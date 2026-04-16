from fastapi import FastAPI
from app.schemas import FactCheckInput
from app.agents.fact_checker import fact_checker_agent
from app.utils.logger import log_run

app = FastAPI(title="Fact Checker Agent")


@app.get("/")
def home():
    return {"message": "Fact Checker Running"}


@app.post("/fact-check")
def fact_check(request: FactCheckInput):
    response = fact_checker_agent(request.dict())

    # log every run (required)
    log_run(response)

    return response