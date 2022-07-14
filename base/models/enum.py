from enum import Enum


class UserAccountRequestType(Enum):
    CREATION = "CREATION"
    DELETION = "DELETION"
    RENEWAL = "RENEWAL"

    @classmethod
    def choices(cls):
        return [(e, e.value) for e in cls]
