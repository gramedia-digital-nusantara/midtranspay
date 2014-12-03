import json
import requests

from . import response


class VTDirect(object):
    '''
    Gateway object that we use to communicate VT-Direct type requests.
    '''
    def __init__(self, server_key, sandbox_mode=False):
        self.server_key = server_key
        self.sandbox_mode = sandbox_mode

    @property
    def base_url(self):
        ''' Returns the Veritrans base URL for API requests.'''
        return 'https://api.sandbox.veritrans.co.id/v2' if self.sandbox_mode \
            else 'https://api.veritrans.co.id/v2'

    def submit_charge_request(self, charge_request):
        '''
        Submits a charge request to the API.  Before submitting, all the
        data in the charge_request is validated and if a failure occurs
        a ValidationError will be raised.
        '''
        # run validation against our charge
        # request before submitting
        charge_request.validate_all()

        # build up our application payload and manually
        # specify the header type.
        payload = json.dumps(charge_request.serialize())
        headers = {'content-type': 'application/json',
                   }

        # now cross our fingers that all went well!
        http_response = requests.post(
            '{base_url}/charges'.format(base_url=self.base_url),
            auth=(self.server_key, ''),
            headers=headers,
            data=payload)

        # send back our response
        veritrans_response = response.Response(**http_response.json())
        return veritrans_response
