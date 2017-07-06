Get Transaction Status
======================

After submitting a charge to Midtrans, you can also check on the status
of a previously-issued transaction.

To look up a previous transaction, you must know the **order_id** of that
transaction.

This only takes 3 steps

.. code-block:: python
    
    from midtranspay import midtrans, request
    from midtranspay.response import status
    
    # 1: Create a gateway to talk to Midtrans
    gateway = midtrans.VTDirect('your-server-key')
    
    # 2: Build a request with the order_id you want to check
    req = request.StatusRequest('the-order-id')
    
    # 3: Get the response
    resp = gateway.submit_status_request(req)
    
    if charge_resp.status_code == status.SUCCESS:
        print("The charge was successful!  We've got their money.")
    elif charge_resp.status_code == status.CHALLENGE:
        print("The transaction was challenged by fraud detection.. "
              "We need to decide whether to accept it or not")
    elif chrage_resp.status_code == status.DENIED:
        print("Their card did not work!")
    else:
        print("Something else: {code}".format(resp.status_code))