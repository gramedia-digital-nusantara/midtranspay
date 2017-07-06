Charge A Customer
=================

Charging a customer is a simple process that involves only 3 steps

.. note::
    Before submitting charges, but must sign create an account with Midtrans
    and have access to your Server Key: `Midtrans Signup`_.
    Also note, please read Midtrans documentation before implementing!
    You cannot submit credit card details from your server -- that must
    be done through a front end javascript library that Midtrans provides.

.. code-block:: python
    
    from midtranspay import midtrans, request, validation, payment_type
    from midtranspay.response import status
    
    # 1: Create a gateway.
    gateway = midtrans.VTDirect('YOUR-API-KEY')

    # 2: Build your Charge Request
    cust = request.CustomerDetails(
        first_name="John",
        last_name="Doe",
        email="john@gmail.com",
        phone="+62 812 1212-1212")
    trans = request.TransactionDetails(
        order_id='1234',
        gross_amount=1200000)
    # NOTE: the token must be retrieved from the midtrans javascript
    # library!!
    cc = payment_type.CreditCard(
        bank='bca',
        token='THE-TOKEN-YOU-GOT')

    # next, we use those 3 entities to build 
    # our complete charge request
    charge_req = request.ChargeRequest(charge_type=cc,
                                       transaction_details=trans,
                                       customer_details=cust)

    
    # 3: Send the charge request to Midtrans and check the response
    try:
        resp = gateway.submit_charge_request(charge_req)
        
        if charge_resp.status_code == status.SUCCESS:
            print("Nice doing business with ya!")
        elif charge_resp.status_code == status.CHALLENGE:
            print("This might be fraud or it might not be.. we have to "
                  "check and approve/cancel the transaction")
        elif chrage_resp.status_code == status.DENIED:
            print("Aduh masbro! Kartu kredit tidak bisa")
        else:
            print("Something else went wrong. "
                  "Better check the resp.status_code")

    catch validation.ValidationError as e:
        print("Oops.. recheck your input.  Something was wrong")

    catch Exception as e:
        # something else entirely went wrong
        # such as a network timeout communicating with midtrans
        print("Uhm.. Bad things")

.. _Midtrans Signup: https://my.midtrans.co.id/register