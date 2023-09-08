from django.http import HttpResponse


def test(request):
    html = "<html><body>%s</body></html>"%"test"
    return HttpResponse(html)
