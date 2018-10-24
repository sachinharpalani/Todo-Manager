from tracking.logging import log_event


class LogEveryEventMiddleware:
        def __init__(self, get_response):
                self.get_response = get_response

        def __call__(self, request):
                log_event(request)

                response = self.get_response(request)

                return response
