.. _index:

Overview
========

Vertranspay is a Python client library for submitting requests to the
http://midtrans.co.id payment gateway.

The only dependency for this library is the `Python Requests`_ package

This library is in a very early stage and only supports credit card charge
requests/responses via the VT-Direct method.  

.. note::
    For developing and testing this library's integration with your own code,
    you will need a **SANDBOX ACCOUNT**, which you can sign up for 
    here: `Midtrans Sandbox Signup`_.

.. warning::
    This software is not associated with or endorsed by Midtrans Indonesia.
    None of the contributers accept any responsiblity for any losses incurred
    by using this software, unless local laws say otherwise.  Use at your own
    risk.

Contents:
---------

.. toctree::
    :maxdepth: 2
    
    quickstart
    charge-a-customer
    get-transaction-status
    approve-reject-challenged-transaction
    api
    changes

Supported Python Versions:
--------------------------

- 2.7
- 3.3
- 3.4

https://travis-ci.org/derekjamescurtis/midtranspay

Testing:
--------

This library comes with a suite of unit tests, as well as live tests that can
run against the *SANDBOX API ONLY*.  This is important to note because VTDirect
will not allow you to generate a charge token and submit a charge request
from the same API on production (however, currently the sandbox DOES allow
this)!

If you're interested in running the live tests, see 
tests/live_credentials.sample for further instructions on how to run these
in the source code of this library.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Midtrans Sandbox Signup: https://my.sandbox.midtrans.co.id/register
.. _Python Requests: https://pypi.python.org/pypi/requests
