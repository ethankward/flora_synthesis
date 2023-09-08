from django.conf import settings
from django.http import HttpResponse


def test(request):
    html = "<html><body>%s</body></html>"%settings.DATABASES
    return HttpResponse(html)
