"""Task state machine. Transitions drive runtime behavior."""

from enum import Enum


class TaskState(str, Enum):
    CREATED = "CREATED"
    PLANNING = "PLANNING"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    VERIFYING = "VERIFYING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


_ALLOWED = {
    TaskState.CREATED: {TaskState.PLANNING, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.PLANNING: {TaskState.READY, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.READY: {TaskState.RUNNING, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.RUNNING: {TaskState.WAITING_APPROVAL, TaskState.VERIFYING, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.WAITING_APPROVAL: {TaskState.RUNNING, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.VERIFYING: {TaskState.PASSED, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.PASSED: set(),
    TaskState.FAILED: {TaskState.RUNNING},
    TaskState.CANCELLED: set(),
}


class InvalidTransition(Exception):
    pass


class StateMachine:
    def __init__(self, initial=TaskState.CREATED):
        self._state = TaskState(initial)
        self.history = [self._state.value]

    @property
    def state(self):
        return self._state

    def transition(self, target):
        target = TaskState(target)
        if target not in _ALLOWED[self._state]:
            raise InvalidTransition(
                "invalid transition %s -> %s" % (self._state.value, target.value)
            )
        self._state = target
        self.history.append(target.value)
        return self._state

    def snapshot(self):
        return {"state": self._state.value, "history": list(self.history)}