from contextvars import ContextVar

from pipeline_statistics.timing_nodes import TimingNode


class TimingTracker:
    def __init__(self):
        self.roots: list[TimingNode] = []
        self.stack: ContextVar[list[TimingNode]] = ContextVar(
            "timing_stack",
            default=[]
        )

    def start(self, caller_name: str) -> TimingNode:
        node = TimingNode(caller_name)
        stack = self.stack.get()

        if stack:
            stack[-1].children.append(node)
        else:
            self.roots.append(node)

        stack.append(node)

        return node

    def finish(self, node: TimingNode, execution_time: float) -> None:
        node.execution_time = execution_time
        stack = self.stack.get()
        stack.pop()

    def to_dict(self) -> dict:
        return {
            node.caller_name: node.to_dict()
            for node in self.roots
        }

timing_tracker = TimingTracker()