import requests


class VTDirect(object):

    def __init__(self, server_key, sandbox_mode=False):
        self.server_key = server_key
        self.sandbox_mode = sandbox_mode

    @property
    def base_url(self):
        ''' Returns the Veritrans base URL for API requests. '''
        return 'https://api.sandbox.veritrans.co.id/v2' if self.sandbox_mode \
            else 'https://api.veritrans.co.id/v2'

    def _build_request(self, request):
        pass

    def submit_charge_request(self, request):

        req = self._build_request(request)
