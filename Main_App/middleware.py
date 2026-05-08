from Admin_App.models import ActiveVisitor
from django.utils.timezone import now

class LocalActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Detect Device
        device = 'desktop'
        if getattr(request, 'user_agent', None):
            if request.user_agent.is_mobile:
                device = 'mobile'
            elif request.user_agent.is_tablet:
                device = 'tablet'

        # 2. Get or create session
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        # 3. Save to SQL Database
        ActiveVisitor.objects.update_or_create(
            session_key=session_key,
            defaults={'device_type': device, 'last_seen': now()}
        )

        return self.get_response(request)
    

############## Production Version #######################

# from django.core.cache import cache

# class ProductionActiveUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # 1. Detect Device AND block bots!
#         if getattr(request, 'user_agent', None) and not request.user_agent.is_bot:
#             device = 'desktop'
#             if request.user_agent.is_mobile:
#                 device = 'mobile'
#             elif request.user_agent.is_tablet:
#                 device = 'tablet'

#             # 2. Get or create session
#             if not request.session.session_key:
#                 request.session.create()
#             session_key = request.session.session_key

#             # 3. Save directly to Redis RAM (expires automatically in 300 seconds)
#             cache.set(f"active_user_{session_key}", device, timeout=300)

#         return self.get_response(request)