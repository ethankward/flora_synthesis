from django.http import HttpResponse
import os


def test(request):
    os.system("python manage.py migrate")

    html = "<html><body>test</body></html>"
    return HttpResponse(html)
