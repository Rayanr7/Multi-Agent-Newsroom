def create_message(run_id, agent_name, input_data, output_data, status):
    from datetime import datetime

    return {
        "run_id": run_id,
        "agent_name": agent_name,
        "timestamp": datetime.utcnow().isoformat(),
        "input": input_data,
        "output": output_data,
        "status": status
    }
