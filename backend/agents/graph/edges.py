from typing import Literal
from agents.graph.state import OrchestrationState

def continue_or_fail(state: OrchestrationState) -> str:
    """
    Checks if there are any errors in the state.
    If errors exist, routes directly to the generate_result node to fail gracefully.
    Otherwise, proceeds to the next node.
    """
    if state.get("errors"):
        return "fail"
    return "continue"
