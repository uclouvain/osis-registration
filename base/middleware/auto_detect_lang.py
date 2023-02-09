from django.utils import translation

from base import settings


class AutoDetectLanguage:
    def __init__(self, response):
        self.response = response

    def __call__(self, request):
        self.auto_detect_french(request)
        response = self.response(request)
        return response

    def auto_detect_french(self, request):
            if "fr" in request.META['HTTP_ACCEPT_LANGUAGE'] and not request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME):
                translation.activate("fr-be")
                request.session[settings.LANGUAGE_COOKIE_NAME] = translation.get_language()
