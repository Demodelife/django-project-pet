def set_useragent_on_request_middleware(get_response):

    print('initial call')

    def middleware(request):
        print('before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get response')

        return response
    return middleware


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exceptions = 0

    def __call__(self, request):
        self.request_count += 1
        print(f'Get requests count {self.request_count}')
        response = self.get_response(request)
        self.response_count += 1
        print(f'Get responses count {self.response_count}')
        return response

    def process_exception(self, request, exception):
        self.exceptions += 1
        print(f'Got {self.exceptions} exc so far')


class SetUserAgentOnRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.user_agent = request.META['HTTP_USER_AGENT']
        response = self.get_response(request)

        return response
