from dataclasses import field, dataclass

from src.utils.formatting.formatting import format_time


@dataclass
class TimingNode:
    caller_name: str
    execution_time: float = 0.0
    children: list["TimingNode"] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            **{
                "execution_time": format_time(round(self.execution_time, 3)
                ),
            },
            **{
                child.caller_name: child.to_dict()
                for child in self.children

         }
        }
