from django.utils.deprecation import MiddlewareMixin

class SMSMiddleware(MiddlewareMixin):
    def process_request(self, request):
        args = request.POST or request.GET
        request.is_sms = args and args.get('MessageSid')
