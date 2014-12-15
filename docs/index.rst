.. _index:

Overview
========

Vertranspay is a Python library for submitting requests to the
http://veritrans.co.id payment gateway.

The only dependency for this library is the `Python Requests`_ package

This library is in a very early stage and only supports credit card charge
requests/responses via the VT-Direct method.  Also, Python 2.7 is the only
version of Python currently supported.

.. note::
    For developing and testing this library's integration with your own code,
    you will need a **SANDBOX ACCOUNT**, which you can sign up for 
    here: `Veritrans Sandbox Signup`_.

This library comes with a suite of unit tests, as well as live tests that can
run against the *SANDBOX API ONLY*.  This is important to note because VTDirect
will not allow you to generate a charge token and submit a charge request
from the same API on production (however, currently the sandbox DOES allow
this)!


.. warning::
    This software is not associated with or endorsed by Veritrans Indonesia.
    None of the contributers accept any responsiblity for any losses incurred
    by using this software, unless local laws say otherwise.  Use at your own
    risk.

Contents:
---------

.. toctree::
    :maxdepth: -1
    
    quickstart
    charge-a-customer
    gateway
    requests
    response


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Veritrans Sandbox Signup: https://my.sandbox.veritrans.co.id/register
.. _Python Requests: https://pypi.python.org/pypi/requests
