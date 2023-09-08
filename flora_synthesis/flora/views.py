from django.http import HttpResponse


def test(request):
    html = "<html><body>test</body></html>"
    return HttpResponse(html)
