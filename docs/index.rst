.. Veritrans Py Client Library documentation master file, created by
   sphinx-quickstart on Tue Dec  2 15:26:36 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Veritranspay - A Python Client Library for Veritrans.co.id
==========================================================

Vertranspay is a Python library for submitting requests to the
http://veritrans.co.id payment gateway.

The only dependency for this library is the `Python Requests`_ package


Before You Start
----------------

For developing and testing this library's integration with your own code,
you will need a **SANDBOX ACCOUNT**, which you can sign up for 
here: `Veritrans Sandbox Signup`_.


Testing
-------

This library comes with a suite of unit tests, as well as live tests that can
run against the *SANDBOX API ONLY*.  This is important to note because VTDirect
will not allow you to generate a charge token and submit a charge request
from the same API on production (however, currently the sandbox DOES allow
this)!


Development Status
------------------

This library is in a very early stage and only supports credit card charge
requests/responses via the VT-Direct method.


Python Version
----------------------

- 2.7.x
- No support yet for Python 3.

Contents:
---------

.. toctree::
   :maxdepth: 2
   
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
