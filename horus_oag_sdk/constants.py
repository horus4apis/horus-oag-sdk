from enum import Enum

class ExecutionSteps:
    """
    Enum for the execution steps.
    """
    INPUT = "input"
    AGGREGATION = "aggregation"
    MODIFY = "modify"
    DROP = "drop"
    GENERATION = "generation"


EXECUTION_STEPS = [
    ExecutionSteps.INPUT,
    ExecutionSteps.AGGREGATION,
    ExecutionSteps.MODIFY,
    ExecutionSteps.DROP,
    ExecutionSteps.GENERATION
]
