import os
import subprocess
import tempfile

from captcha.conf import settings
from captcha.models import CaptchaStore
from django.http import HttpResponse, Http404
from django.utils import translation
from ranged_response import RangedFileResponse


def captcha_audio(request, key):
    if settings.CAPTCHA_FLITE_PATH:
        try:
            store = CaptchaStore.objects.get(hashkey=key)
        except CaptchaStore.DoesNotExist:
            # HTTP 410 Gone status so that crawlers don't index these expired urls.
            return HttpResponse(status=410)

        text = store.challenge
        if "captcha.helpers.math_challenge" == settings.CAPTCHA_CHALLENGE_FUNCT:
            text = text.replace("*", "times").replace("-", "minus").replace("+", "plus")
        else:
            text = ", ".join(list(text))
        path = str(os.path.join(tempfile.gettempdir(), "%s.wav" % key))
        language = translation.get_language()
        subprocess.call([settings.CAPTCHA_FLITE_PATH, "-v", language, text, "-s", "100", "-w", path])

        # Add arbitrary noise if sox is installed
        if settings.CAPTCHA_SOX_PATH:
            arbnoisepath = str(
                os.path.join(tempfile.gettempdir(), "%s_arbitrary.wav") % key
            )
            mergedpath = str(os.path.join(tempfile.gettempdir(), "%s_merged.wav") % key)
            subprocess.call(
                [
                    settings.CAPTCHA_SOX_PATH,
                    "-r",
                    "22050",
                    "-n",
                    arbnoisepath,
                    "synth",
                    "2",
                    "brownnoise",
                    "gain",
                    "-15",
                ]
            )
            subprocess.call(
                [
                    settings.CAPTCHA_SOX_PATH,
                    "-m",
                    arbnoisepath,
                    path,
                    "-t",
                    "wavpcm",
                    "-b",
                    "16",
                    mergedpath,
                ]
            )
            os.remove(arbnoisepath)
            os.remove(path)
            os.rename(mergedpath, path)

        if os.path.isfile(path):
            response = RangedFileResponse(
                request, open(path, "rb"), content_type="audio/wav"
            )
            response["Content-Disposition"] = 'attachment; filename="{}.wav"'.format(key)
            return response
    raise Http404
