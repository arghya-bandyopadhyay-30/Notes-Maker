from dataclasses import field, dataclass

from src.utils.formatting.formatting import format_time
from src.utils.formatting.strings import TIMING_EXECUTION_TIME_KEY


@dataclass
class TimingNode:
    caller_name: str
    execution_time: float = 0.0
    children: list["TimingNode"] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            **{
                TIMING_EXECUTION_TIME_KEY: format_time(round(self.execution_time, 3)
                ),
            },
            **{
                child.caller_name: child.to_dict()
                for child in self.children

         }
        }
