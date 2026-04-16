import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.orchestrator import run_pipeline

def run_evaluation():
    # Load test scenarios
    #with open("test_scenarios.json", "r") as f:
        #scenarios = json.load(f)

    # Define absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    logs_dir = os.path.join(base_dir, "logs")
    logs_path = os.path.join(logs_dir, "runs.json")

    # Ensure logs directory exists
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        # Initialize the file with an empty list if it doesn't exist
        with open(logs_path, "w") as f:
            json.dump([], f)

    # Load test scenarios
    # (Assuming test_scenarios.json is in the same folder as this script)
    scenario_path = os.path.join(os.path.dirname(__file__), "test_scenarios.json")
    with open(scenario_path, "r") as f:
        scenarios = json.load(f)
    results = []
    correct_detections = 0
    total_bad = 0
    total_rejected = 0

    for scenario in scenarios:
        print(f"Running scenario {scenario['id']}: {scenario['topic']}...")

        try:
            result = run_pipeline(scenario["topic"], scenario["seed"])
            run_id = result["run_id"]
            final_state = result["final_state"]
            
            if not os.path.exists(logs_path):
                print(f"  ❌ ERROR: Orchestrator failed to create {logs_path}")
                continue

            # Read the latest log to get credibility score and verdict
            #with open("../logs/runs.json", "r") as f:
            #logs_path = os.path.join(os.path.dirname(__file__), "..", "logs", "runs.json")
            with open(logs_path, "r") as f:
                logs = json.load(f)

            # Find logs for this run
            run_logs = [l for l in logs if l["run_id"] == run_id]

            # Extract fact checker output
            fc_log = next((l for l in run_logs if l["agent_name"] == "FACT_CHECKER"), None)
            credibility_score = fc_log["output"]["credibility_score"] if fc_log else None
            verdict = fc_log["output"]["verdict"] if fc_log else None

            # Extract editor decision
            ed_log = next((l for l in run_logs if l["agent_name"] == "EDITOR"), None)
            decision = ed_log["output"]["decision"] if ed_log else None

            # Track metrics
            if scenario["type"] in ["misinformation", "vague_sources"]:
                total_bad += 1
                if verdict in ["WARN", "FAIL"]:
                    correct_detections += 1

            if decision == "REJECTED":
                total_rejected += 1

            scenario_result = {
                "id": scenario["id"],
                "topic": scenario["topic"],
                "seed": scenario["seed"],
                "expected_verdict": scenario["expected_verdict"],
                "actual_verdict": verdict,
                "credibility_score": credibility_score,
                "decision": decision,
                "final_state": final_state,
                "verdict_match": verdict == scenario["expected_verdict"]
            }

        except Exception as e:
            print(f"  ERROR DETAIL: {e}")
            scenario_result = {
                "id": scenario["id"],
                "topic": scenario["topic"],
                "seed": scenario["seed"],
                "expected_verdict": scenario["expected_verdict"],
                "actual_verdict": "ERROR",
                "credibility_score": None,
                "decision": "ERROR",
                "final_state": "ERROR",
                "verdict_match": False,
                "error": str(e)
            }

        results.append(scenario_result)
        print(f"  → Verdict: {scenario_result['actual_verdict']} | Score: {scenario_result['credibility_score']} | Decision: {scenario_result['decision']}")

    # Calculate final metrics
    valid_scores = [r["credibility_score"] for r in results if r["credibility_score"] is not None]
    avg_credibility = round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else 0
    detection_rate = round((correct_detections / total_bad) * 100, 2) if total_bad > 0 else 0
    rejection_rate = round((total_rejected / len(scenarios)) * 100, 2)

    summary = {
        "total_scenarios": len(scenarios),
        "avg_credibility_score": avg_credibility,
        "misinformation_detection_rate": f"{detection_rate}%",
        "editor_rejection_rate": f"{rejection_rate}%",
        "verdict_accuracy": f"{round(sum(r['verdict_match'] for r in results) / len(results) * 100, 2)}%"
    }

    output = {
        "summary": summary,
        "results": results
    }

    with open("evaluation_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\n=== EVALUATION SUMMARY ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print("\nFull results saved to evaluation_results.json")

if __name__ == "__main__":
    run_evaluation()
