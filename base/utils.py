from enum import Enum

from django.utils.translation import gettext_lazy as _


class PasswordCheckErrorEnum(Enum):
    TOO_SHORT = {
        "code": 1, "msg": _("Password too short (less than 12 characters)")
    }
    TOO_LONG = {
        "code": 2, "msg": _("Password too long (more than 200 characters)")
    }
    UNSUPPORTED_CHAR = {
        "code": 3, "msg": _("Some unsupported characters are present in the password")
    }
    NOT_ENOUGH_DIVERSITY = {
        "code": 4, "msg": _("Not enough character diversity in the password. Please provide"
                            " at least 3 characters types among uppercase, lowercase, digit and special")
    }
    SIMILAR_TO_FIRSTNAME_LAST_NAME = {
        "code": 5, "msg": _("The password is too similar to first name or last name")
    }
    CORRUPTED = {
        "code": 6, "msg": _("This password has been found in a password database leaked publicly")
    }
    MISSING_PARAMETERS = {
        "code": 99, "msg": _("Some parameters are missing for the password check")
    }

    @staticmethod
    def get_error_msg(code):
        error_msg_mapping = {s.value["code"]: s.value["msg"] for s in PasswordCheckErrorEnum}
        return error_msg_mapping[code]


class PasswordCheckServiceBadRequestException(Exception):
    msg = "The request to the password check service is bad formatted"
