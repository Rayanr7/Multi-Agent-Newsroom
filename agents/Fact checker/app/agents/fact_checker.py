from datetime import datetime
from app.services.scoring_service import calculate_score, get_verdict


def fact_checker_agent(input_data: dict):
    score, flagged_claims, flagged_sources = calculate_score(
        body=input_data["body"],
        sources=input_data["claimed_sources"],
        entities=input_data["named_entities"]
    )

    verdict = get_verdict(score)

    output = {
        "credibility_score": score,
        "flagged_claims": flagged_claims,
        "flagged_sources": flagged_sources,
        "verdict": verdict
    }

    return {
        "run_id": input_data["run_id"],
        "agent_name": "fact_checker",
        "timestamp": datetime.utcnow().isoformat(),
        "input": input_data,
        "output": output,
        "status": "SUCCESS"
    }