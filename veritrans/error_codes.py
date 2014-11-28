''' Represents the different HTTP status codes
returned from the API to indicate errors.

http://docs.veritrans.co.id/sandbox/charge.html#error-on-transaction-charge
'''

VALIDATION_ERROR = 400
ACCESS_DENIED = 401
# note: documented as 'Access Denied' but this is more descriptive
UNAVAILABLE_PAYMENT_TYPE = 402
DUPLICATE_ORDER_ID = 406
ACCOUNT_INACTIVE = 410
TOKEN_ERROR = 411