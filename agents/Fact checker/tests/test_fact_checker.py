from app.agents.fact_checker import fact_checker_agent


def test_low_credibility():
    input_data = {
        "run_id": "test1",
        "headline": "Fake News",
        "body": "Anonymous sources say FakeCorp is real.",
        "claimed_sources": ["Random Blog"],
        "named_entities": ["FakeCorp"]
    }

    result = fact_checker_agent(input_data)

    assert result["output"]["credibility_score"] < 50
    assert result["output"]["verdict"] in ["WARN", "FAIL"]