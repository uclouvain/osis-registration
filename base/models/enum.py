from enum import Enum


class UserAccountRequestType(Enum):
    CREATION = "CREATION"
    DELETION = "DELETION"
    RENEWAL = "RENEWAL"

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class UserAccountRequestStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    PENDING = "PENDING"

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class UserPasswordResetRequestStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    PENDING = "PENDING"

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)
