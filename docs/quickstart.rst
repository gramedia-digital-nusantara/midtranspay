Quick Start
============================

Once the library is installed and on your python path you will need to sign
up for an account on Veritrans.

from veritrans import veritrans, request, payment_types


# create a gateway instance
gateway = veritrans.VTDirect(api_key='YOU-API-KEY')


# build the request --
# first we start with the 3 sub-entities
cust = request.CustomerDetails()
trans = request.TransactionDetails()
cc = payment_type.CreditCard()

# next, we use those 3 entities to build 
# our complete charge request
charge_req = request.ChargeRequest(charge_type=cc,
                                   transaction_details=trans,
                                   customer_details=cust)


# lastly, we send our charge request to our gateway
resp = gateway.submit_charge_request(charge_req)