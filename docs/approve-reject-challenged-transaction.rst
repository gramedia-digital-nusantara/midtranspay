Approve/Reject a Challenged Transaction
=======================================

Veritrans implements it's own fraud detection system.  Sometimes, even if
a credit card can be charged, Veritrans will set the transaction as Challenge
(201).

Those transactions can manually be approved through the MAP website, or can
be handled by your code.

.. code-block:: python
    
    from veritranspay import veritrans, request, validation, payment_type
    from veritranspay.response import status
    
    # 1: Create a gateway
    gateway = veritrans.VTDirect('YOUR-API-KEY')

    # 2: Build a charge request (params omitted)
    charge_req = request.ChargeRequest(**your_charge_req_args)

    # lastly, we send our charge request to our gateway
    resp = gateway.submit_charge_request(charge_req)
    
    if charge_resp.status_code == status.SUCCESS:
        # We can't approve/cancel a SUCCESS transaction
        pass
    elif charge_resp.status_code == status.CHALLENGE:
        
        # 4: Decision time -- approve or cancel?
        CANCEL_CHALLENGE_TRANSACTIONS = True
        
        if CANCEL_CHALLENGE_TRANSACTIONS:
            # We can pass our charge response straight back to the 
            # submit_cancel_request method.
            # We can also do this with a StatusResponse, OR we can build
            # a special request.CancelRequest/ApprovalRequest object and pass
            # that to the gateway.  They will all work just as well.
            new_resp = gateway.submit_cancel_request(resp)
        
        else:
            # if we we're approving it, we can do that as well.
            # this time, let's create a special ApprovalRequest object
            # (although we could just use the CreditCardChargeResponse, like
            # we did above).
            approval_req = request.ApprovalRequest(order_id=resp.order_id)
            new_resp = gateway.submit_approval_request(approval_req)
            
    elif chrage_resp.status_code == status.DENIED:
        # We can't approve a DENIED transaction
        pass
