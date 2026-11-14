from dataclasses import dataclass


@dataclass(init=False)
class Stats:
    already_handled: int = 0
    not_handled: int = 0
    handled: int = 0
    filecount: int = 0
