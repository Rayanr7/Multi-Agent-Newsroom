from orchestrator.state_machine import StateMachine
from orchestrator.utils import generate_run_id
from orchestrator.logger import log_event
from schemas.message_schemas import create_message

from agents import reporter, fact_checker, editor, publisher

import random


def run_pipeline(topic, seed):
    random.seed(seed)

    sm = StateMachine()
    run_id = generate_run_id()

    # REPORTER
    sm.transition("REPORTING")
    reporter_input = {
        "topic": topic,
        "seed": seed
    }
    reporter_output = reporter.run(reporter_input)

    msg1 = create_message(run_id, "REPORTER", reporter_input, reporter_output, "SUCCESS")
    log_event(msg1)

    # FACT CHECK
    sm.transition("FACT_CHECKING")
    fact_input = reporter_output
    fact_output = fact_checker.run(fact_input)

    msg2 = create_message(run_id, "FACT_CHECKER", fact_input, fact_output, "SUCCESS")
    log_event(msg2)

    # EDITOR (FIXED PROPERLY)
    sm.transition("EDITING")
    editor_input = {
        "reporter_output": reporter_output,
        "fact_checker_output": fact_output
    }
    editor_output = editor.run(editor_input)

    msg3 = create_message(run_id, "EDITOR", editor_input, editor_output, "SUCCESS")
    log_event(msg3)

    # FINAL STATE
    if editor_output["decision"] == "REJECTED":
        sm.transition("REJECTED")
    else:
        sm.transition("PUBLISHED")

    # PUBLISHER
    publisher_input = editor_output
    publisher_output = publisher.run(publisher_input)

    msg4 = create_message(run_id, "PUBLISHER", publisher_input, publisher_output, "SUCCESS")
    log_event(msg4)

    return {
        "run_id": run_id,
        "final_state": sm.state,
        "output": publisher_output
    }