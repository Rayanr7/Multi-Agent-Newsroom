from orchestrator.utils import generate_run_id
from schemas.message_schemas import create_message
from orchestrator.logger import log_event
from orchestrator.state_machine import StateMachine

from agents import reporter, fact_checker, editor, publisher


def run_pipeline(topic, seed):
    run_id = generate_run_id()
    sm = StateMachine()

    # REPORTER
    sm.transition("REPORTING")
    rep_out = reporter.run({"topic": topic, "seed": seed})

    rep_msg = create_message(run_id, "REPORTER", {"topic": topic}, rep_out, "SUCCESS")
    log_event(rep_msg)

    # FACT CHECKER
    sm.transition("FACT_CHECKING")
    fc_out = fact_checker.run(rep_out)

    fc_msg = create_message(run_id, "FACT_CHECKER", rep_out, fc_out, "SUCCESS")
    log_event(fc_msg)

    # EDITOR
    sm.transition("EDITING")
    ed_out = editor.run(rep_out, fc_out)

    ed_msg = create_message(run_id, "EDITOR", fc_out, ed_out, "SUCCESS")
    log_event(ed_msg)

    # FINAL STATE
    if ed_out["decision"] == "REJECTED":
        sm.transition("REJECTED")
    else:
        sm.transition("PUBLISHED")
        pub_out = publisher.run(ed_out)

        pub_msg = create_message(run_id, "PUBLISHER", ed_out, pub_out, "SUCCESS")
        log_event(pub_msg)

    return {"run_id": run_id, "final_state": sm.state}