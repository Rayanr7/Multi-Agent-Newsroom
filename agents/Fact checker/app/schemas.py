from pydantic import BaseModel
from typing import List, Dict


class FactCheckInput(BaseModel):
    run_id: str
    headline: str
    body: str
    claimed_sources: List[str]
    named_entities: List[str]


class FactCheckOutput(BaseModel):
    credibility_score: int
    flagged_claims: List[str]
    flagged_sources: List[str]
    verdict: str


class AgentResponse(BaseModel):
    run_id: str
    agent_name: str
    timestamp: str
    input: Dict
    output: Dict
    status: str