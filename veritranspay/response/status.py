'''
Represents the different HTTP status codes
returned from the API to indicate errors.

http://docs.veritranspay.co.id/sandbox/status_code.html
'''
# 20x - successful submission to api
SUCCESS = 200
CHALLENGE = 201
DENIED = 202


# 30x
MOVED_PERMANENTLY = 300


# 40x
VALIDATION_ERROR = 400
ACCESS_DENIED = 401
# note: documented as 'Access Denied' but this is more descriptive
# and that would also create two 'Access Denied'
UNAVAILABLE_PAYMENT_TYPE = 402
DUPLICATE_ORDER_ID = 406
ACCOUNT_INACTIVE = 410
TOKEN_ERROR = 411



# 50x
SERVER_ERROR = 500
FEATURE_UNAVAILABLE = 501
BANK_CONNECTION_PROBLEM = 502
SERVER_ERROR_OTHER = 503
FRAUD_DETECTION_UNAVAILABLE = 504