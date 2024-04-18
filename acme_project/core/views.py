from django.shortcuts import render


def page_not_found(request, exception):
    """Страница ошибки 404."""
    return render(request, 'core/404.html', status=404)

def csrf_failure(request, reason=''):
    """Страница ошибки 403."""
    return render(request, 'core/403csrf.html', status=403)
