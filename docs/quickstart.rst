Quick Start
===========

From this point on, we're going to assume that you've signed up for an account
with Midtrans (if not, go back to the index page of this documentation),
and that you've successfully installed this library somewhere on your python
path.

Here is a *mostly-complete* short script that will give you an overview of
how to use the library.  The only feature that is omitted are the init
arguments you'll need to provide to 3 objects (CustomerDetails,
TransactionDetails, and CreditCard).  All three are explained in more 
detail in --this.. link to the section-- Section.

.. code-block:: python
    
    from midtranspay import midtrans, request, validation, payment_type
    from midtranspay.response import status
    
    # this gateway will submit to the sandbox API.
    gateway = midtrans.VTDirect(api_key='YOUR-API-KEY', sandbox_mode=True)

    # constructor args are omitted here for brevity
    # see sections that follow for more details about building
    # individual entity types
    cust = request.CustomerDetails(**cust_args)
    trans = request.TransactionDetails(**trans_args)
    cc = payment_type.CreditCard(**cc_args)

    # next, we use those 3 entities to build 
    # our complete charge request
    charge_req = request.ChargeRequest(charge_type=cc,
                                       transaction_details=trans,
                                       customer_details=cust)

    
    # lastly, we send our charge request to our gateway
    try:
        charge_resp = gateway.submit_charge_request(charge_req)
        
        if charge_resp.status_code == status.SUCCESS:
            # yay!
            print("GREAT SUCCESS!!  We've got your money!  Hope you ordered "
                  "something nice!")
        elif charge_resp.status_code == status.CHALLENGE:
            # the payment was accepted, but you'll have to manually validate
            # and approve the transation through http://my.midtrans.co.id
            print("Your transaction is approved, but we need to "
                  "check some things out.. just you wait, OK?")
        elif chrage_resp.status_code == status.DENIED:
            # bad!
            print("Aduh masbro! Kartu kredit tidak bisa")
        else:
            # something else entirely
            print("...Aduh.  Pusing.  Tunggu ya?")

    catch validation.ValidationError as e:
        # We failed client-side validation
        # This happens automatically before our request is submitted to
        # midtrans!
        print("Oops.. you need to check your data")

    catch Exception as e:
        # something else entirely went wrong
        print("Uhm.. Bad things")

Ok, so that's that!
    