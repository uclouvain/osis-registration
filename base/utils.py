from enum import Enum

from django.utils.translation import gettext_lazy as _


class PasswordCheckErrorEnum(Enum):
    TOO_SHORT = 1, _("Password too short (less than 12 characters)")
    TOO_LONG = 2, _("Password too long (more than 200 characters)")
    UNSUPPORTED_CHAR = 3, _("Some unsupported characters are present in the password")
    NOT_ENOUGH_DIVERSITY = 4, _("Not enough character diversity in the password. "
                                "Please provide at least 3 characters types among "
                                "uppercase, lowercase, digit and special")
    SIMILAR_TO_FIRSTNAME_LAST_NAME = 5, _("The password is too similar to first name or last name")
    CORRUPTED = 6, _("This password has been found in a password database leaked publicly")
    MISSING_PARAMETERS = 99, _("Some parameters are missing for the password check")

    @staticmethod
    def get_error_msg(code):
        error_msg_mapping = {error_code: text for error_code, text in PasswordCheckErrorEnum.values()}
        return error_msg_mapping[code]

    @staticmethod
    def values():
        return [item.value for item in PasswordCheckErrorEnum]


class PasswordCheckServiceBadRequestException(Exception):
    msg = "The request to the password check service is bad formatted"
