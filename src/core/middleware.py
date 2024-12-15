import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.utils.timezone import now

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the last activity timestamp
        last_activity = request.session.get('last_activity')
        if last_activity:
            elapsed_time = (now() - datetime.datetime.fromisoformat(last_activity)).total_seconds()
            if elapsed_time > settings.SESSION_COOKIE_AGE:
                logout(request)  # Logout the user
                request.session.flush()  # Clear the session

        # Update the last activity timestamp
        request.session['last_activity'] = now().isoformat()

        response = self.get_response(request)
        return response
