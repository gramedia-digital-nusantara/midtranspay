.. Veritrans Py Client Library documentation master file, created by
   sphinx-quickstart on Tue Dec  2 15:26:36 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Veritranspay - A Python Client Library for Veritrans.co.id
==========================================================

VertransPy is a python library for submitting requests to the
veritrans.co.id payment gateway.

Before You Start
----------------

For developing and testing this library's integration with your own code,
you will need a *SANDBOX ACCOUNT*, which you can sign up for 
here: VeritransSandboxSignup_.


Testing
-------

This library comes with a suite of unit tests, as well as live tests that can
run against the *SANDBOX API ONLY*.  This is important to note because VTDirect
will not allow you to generate a charge token and submit a charge request
from the same API on production (however, currently the sandbox DOES allow
this)!

Development Status
------------------

This library is in a very early stage and only supports requests
submitted to the 

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _VeritransSandboxSignup: https://my.sandbox.veritrans.co.id/register
