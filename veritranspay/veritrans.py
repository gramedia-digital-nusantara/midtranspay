import json
import requests
from . import response


class VTDirect(object):
    '''
    Gateway object that we use to communicate VT-Direct type requests.
    '''
    LIVE_API_URL = 'https://api.veritrans.co.id/v2'
    SANDBOX_API_URL = 'https://api.sandbox.veritrans.co.id/v2'

    def __init__(self, server_key, sandbox_mode=False):
        self.server_key = server_key
        self.sandbox_mode = sandbox_mode

    @property
    def base_url(self):
        '''
        Returns the Veritrans base URL for API requests.  This will
        differ depending on whether sandbox_mode is enabled or not.
        '''
        return VTDirect.SANDBOX_API_URL if self.sandbox_mode \
            else VTDirect.LIVE_API_URL

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
                   'accept': 'application/json',
                   }

        # now cross our fingers that all went well!
        http_response = requests.post(
            '{base_url}/charge'.format(base_url=self.base_url),
            auth=(self.server_key, ''),
            headers=headers,
            data=payload)

        response_json = http_response.json()

        veritrans_response = response.build_charge_response(
            request=charge_request,
            **response_json)

        return veritrans_response

    def submit_status_request(self, status_request):
        '''
        Gets the status from veritrans for a single transaction.
        '''
        status_request.validate_all()

        request_url_format = '{base_url}/{order_id}/status'

        headers = {'accept': 'application/json',
                   }

        http_response = requests.get(
           request_url_format.format(
               base_url=self.base_url,
               order_id=status_request.order_id),
           auth=(self.server_key, ''),
           headers=headers)

        response_json = http_response.json()

        veritrans_response = response.StatusResponse(**response_json)

        return veritrans_response

    def submit_cancel_request(self, cancel_request):
        '''
        Sends a request to Veritrans to cancel a single transaction.
        '''
        cancel_request.validate_all()

        request_url_format = '{base_url}/{order_id}/cancel'

        headers = {'accept': 'application/json',
                   }

        http_response = requests.post(
           request_url_format.format(
               base_url=self.base_url,
               order_id=cancel_request.order_id),
           auth=(self.server_key, ''),
           headers=headers)

        response_json = http_response.json()

        veritrans_response = response.CancelResponse(**response_json)

        return veritrans_response

    def submit_approval_request(self, approval_request):
        '''
        Sends a request to Veritrans to approve a single, challenged
        transaction.
        '''
        approval_request.validate_all()

        request_url_format = '{base_url}/{order_id}/approve'

        headers = {'accept': 'application/json',
                   }

        http_response = requests.post(
           request_url_format.format(
               base_url=self.base_url,
               order_id=approval_request.order_id),
           auth=(self.server_key, ''),
           headers=headers)

        response_json = http_response.json()

        veritrans_response = response.ApprovalResponse(**response_json)

        return veritrans_response

    def __repr__(self):
        return ("<VTDirect("
                "server_key: '{server_key}', "
                "sandbox_mode: {sandbox_mode})>"
                .format(server_key=self.server_key,
                        sandbox_mode=self.sandbox_mode))
