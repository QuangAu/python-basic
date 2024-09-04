import enum


class PlayerPosition(enum.Enum):
    GOALKEEPER = "GK"
    CENTERBACK = "CB"
    MIDFIELDER = "MF"
    FORWARD = "FW"

    @classmethod
    def to_string(cls):
        return ", ".join(f"{e.value} for {e.name}" for e in PlayerPosition)
