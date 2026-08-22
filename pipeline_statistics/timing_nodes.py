from dataclasses import field, dataclass


@dataclass
class TimingNode:
    caller_name: str
    execution_time: float = 0.0
    children: list["TimingNode"] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            **{
                "execution_time": (
                    f"{round(self.execution_time, 3)} sec"
                ),
            },
            **{
                child.caller_name: child.to_dict()
                for child in self.children

         }
        }
