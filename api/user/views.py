from django.http.response import JsonResponse


def test(request):
    return JsonResponse({"test": "pass"})
