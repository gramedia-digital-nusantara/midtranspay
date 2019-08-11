import json
import requests
from . import response


class VTDirect(object):
    '''
    Gateway used to submit requests to Veritrans via the VTDirect method.
    '''
    LIVE_API_URL = 'https://api.midtrans.com/v2'
    SANDBOX_API_URL = 'https://api.sandbox.midtrans.com/v2'

    def __init__(self, server_key, sandbox_mode=False):
        '''
        :param server_key: Your Veritrans account server key.
        :type server_key: :py:class:`str`
        :param sandbox_mode: If True, requests will be submitted to the
            Veritrans sandbox API, instead of the live API.
        :type sandbox_mode: :py:class:`bool`
        '''
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

    def submit_charge_request(self, req):
        '''
        Submits a charge request to the API.  Before submitting, all the
        data in the req is validated and if a failure occurs
        a ValidationError will be raised.

        :param req: Information about a transaction and a customer to charge.
        :type req: :py:class:`veritranspay.request.ChargeRequest`
        :rtype: :py:class:`veritranspay.response.response.ChargeResponseBase`
        '''
        # run validation against our charge
        # request before submitting
        req.validate_all()

        # build up our application payload and manually
        # specify the header type.
        payload = json.dumps(req.serialize())
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
            request=req,
            **response_json)

        return veritrans_response

    def submit_status_request(self, req):
        '''
        Retrieve information from Veritrans about a single transaction.

        :param req: Data about a transaction to retrieve the status of.
        :type req: :py:class:`veritranspay.request.StatusRequest` **or** Any
            response class that has an order_id attribute, such as
            :py:class:`veritranspay.response.response.ChargeResponseBase`
        :rtype: :py:class:`veritranspay.response.response.StatusResponse`
        '''
        # specifically skip if it's a response type
        # we don't have a good reason to validate those.
        if not isinstance(req, response.ResponseBase):
            req.validate_all()

        request_url_format = '{base_url}/{order_id}/status'

        headers = {'accept': 'application/json',
                   }

        http_response = requests.get(
            request_url_format.format(
                base_url=self.base_url,
                order_id=req.order_id),
            auth=(self.server_key, ''),
            headers=headers)

        response_json = http_response.json()

        veritrans_response = response.StatusResponse(**response_json)

        return veritrans_response

    def submit_cancel_request(self, req):
        '''
        Sends a request to Veritrans to cancel a single transaction.

        :param req: Data about a transaction to cancel.
        :type req: :py:class:`veritranspay.request.CancelRequest` **or** Any
            response class that has an order_id attribute, such as
            :py:class:`veritranspay.response.response.ChargeResponseBase`
        :rtype: :py:class:`veritranspay.response.response.CancelResponse`
        '''
        # specifically skip if it's a response type
        # we don't have a good reason to validate those.
        if not isinstance(req, response.ResponseBase):
            req.validate_all()

        request_url_format = '{base_url}/{order_id}/cancel'

        headers = {'accept': 'application/json',
                   }

        http_response = requests.post(
            request_url_format.format(
                base_url=self.base_url,
                order_id=req.order_id),
            auth=(self.server_key, ''),
            headers=headers)

        response_json = http_response.json()

        veritrans_response = response.CancelResponse(**response_json)

        return veritrans_response

    def submit_approval_request(self, req):
        '''
        Sends a request to Veritrans to approve a single, challenged
        transaction.

        :param req: Data about a transaction to approve.
        :type req: :py:class:`veritranspay.request.ApprovalRequest` **or** Any
            response class that has an order_id attribute, such as
            :py:class:`veritranspay.response.response.ChargeResponseBase`
        :rtype: :py:class:`veritranspay.response.response.ApproveResponse`
        '''
        # specifically skip if it's a response type
        # we don't have a good reason to validate those.
        if not isinstance(req, response.ResponseBase):
            req.validate_all()

        request_url_format = '{base_url}/{order_id}/approve'

        headers = {'accept': 'application/json',
                   }

        http_response = requests.post(
            request_url_format.format(
                base_url=self.base_url,
                order_id=req.order_id),
            auth=(self.server_key, ''),
            headers=headers)

        response_json = http_response.json()

        veritrans_response = response.ApproveResponse(**response_json)

        return veritrans_response

    def bin_request(self, req):
        '''
        Send a request to Veritrans to get bin info
        :param req: Bin number of credit card.
        :type req: :py:class:`veritranspay.request.BinsRequest`
        :rtype: :py:class:`veritranspay.response.response.BinResponse`
        '''
        if not isinstance(req, response.ResponseBase):
            req.validate_all()

        headers = {
            'accept': 'application/json',
        }

        http_response = requests.get(
            '{base_url}/bins/{bin_number}'.format(
                base_url=self.base_url.replace('v2', 'v1'), bin_number=req.bin_number
            ),
            auth=(self.server_key, ''),
            headers=headers
        )

        response_json = http_response.json()
        status_code = http_response.status_code
        response_json['status_code'] = status_code
        if status_code != 200:
            response_json['status_message'] = 'failed'
        else:
            response_json['status_message'] = ''

        veritrans_response = response.BinResponse(**response_json)

        return veritrans_response


    def __repr__(self):
        return ("<VTDirect("
                "server_key: '{server_key}', "
                "sandbox_mode: {sandbox_mode})>"
                .format(server_key=self.server_key,
                        sandbox_mode=self.sandbox_mode))
