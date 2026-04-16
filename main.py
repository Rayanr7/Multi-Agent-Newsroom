from orchestrator.runner import run_pipeline

if __name__ == "__main__":
    topic = "climate change"
    seed = 42

    result = run_pipeline(topic, seed)
    print(result)
