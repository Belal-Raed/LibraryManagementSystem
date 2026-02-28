from .models import VisitLog


class VisitLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/static/') and not request.path.startswith('/media/'):
            try:
                VisitLog.objects.create(
                    path=request.path,
                    method=request.method,
                    ip_address=self.get_client_ip(request),
                    user=request.user if request.user.is_authenticated else None,
                )
            except Exception:
                pass 

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
