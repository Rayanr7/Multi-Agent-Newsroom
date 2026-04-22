import random
import uuid
from datetime import datetime

# -----------------------------
# CONFIG DATA (10 TOPIC TYPES)
# -----------------------------

TOPIC_TEMPLATES = {
    "politics": [
        "Government announces new policy on {topic}.",
        "Leaders debate over {topic} in parliament.",
        "New reforms introduced regarding {topic}."
    ],
    "health": [
        "Health experts warn about rising concerns in {topic}.",
        "New study reveals insights on {topic}.",
        "WHO releases report on {topic}."
    ],
    "technology": [
        "Tech companies innovate around {topic}.",
        "Breakthrough achieved in {topic}.",
        "Startups disrupt market with {topic}."
    ],
    "sports": [
        "Team achieves milestone in {topic}.",
        "Star player shines in {topic}.",
        "Championship highlights include {topic}."
    ],
    "economy": [
        "Market trends shift due to {topic}.",
        "Economists analyze impact of {topic}.",
        "Stock markets react to {topic}."
    ],
    "science": [
        "Scientists discover new findings in {topic}.",
        "Research study published on {topic}.",
        "New experiment advances {topic}."
    ],
    "environment": [
        "Climate activists raise concerns about {topic}.",
        "Environmental report highlights {topic}.",
        "New policies aim to control {topic}."
    ],
    "crime": [
        "Authorities investigate case related to {topic}.",
        "Police report incident involving {topic}.",
        "New developments in {topic} case."
    ],
    "entertainment": [
        "Celebrity news highlights {topic}.",
        "Film industry buzzes around {topic}.",
        "New release focuses on {topic}."
    ],
    "international": [
        "Global leaders discuss {topic}.",
        "International summit focuses on {topic}.",
        "Diplomatic talks involve {topic}."
    ]
}

SOURCES = [
    "Reuters", "BBC", "WHO", "NASA",
    "Anonymous Insider", "Local News", "Sources say"
]

ENTITIES = [
    "United Nations", "India", "USA", "Elon Musk",
    "World Health Organization", "NASA", "Government Officials"
]


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def generate_run_id():
    return str(uuid.uuid4())


def current_timestamp():
    return datetime.utcnow().isoformat()


def detect_category(topic):
    topic = topic.lower()
    for category in TOPIC_TEMPLATES:
        if category in topic:
            return category
    return random.choice(list(TOPIC_TEMPLATES.keys()))


# -----------------------------
# MAIN REPORTER AGENT
# -----------------------------

def reporter_agent(topic, seed):
    random.seed(seed)

    run_id = generate_run_id()
    timestamp = current_timestamp()

    category = detect_category(topic)

    # Generate headline
    headline = f"{topic.title()} — Major Update"

    # Generate body (3–5 sentences)
    sentences = []
    num_sentences = random.randint(3, 5)

    for _ in range(num_sentences):
        template = random.choice(TOPIC_TEMPLATES[category])
        sentence = template.format(topic=topic)
        sentences.append(sentence)

    body = " ".join(sentences)

    # Select sources
    claimed_sources = random.sample(SOURCES, random.randint(2, 4))

    # Select named entities
    named_entities = random.sample(ENTITIES, random.randint(2, 4))

    # -----------------------------
    # OUTPUT JSON (STRICT SCHEMA)
    # -----------------------------
    output = {
        "headline": headline,
        "body": body,
        "claimed_sources": claimed_sources,
        "named_entities": named_entities
    }

    message = {
        "run_id": run_id,
        "agent_name": "REPORTER",
        "timestamp": timestamp,
        "input": {
            "topic": topic,
            "seed": seed
        },
        "output": output,
        "status": "SUCCESS"
    }

    return message


# -----------------------------
# TEST RUN
# -----------------------------
if __name__ == "__main__":
    topic = "climate change"
    seed = 42

    result = reporter_agent(topic, seed)

    import json
    print(json.dumps(result, indent=4))