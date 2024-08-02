from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        # Replace with the external URL you want to redirect to (allows hosting on localhost & redirects to work properly)
        return 'https://www.dhsclubs.org/clubs/'
