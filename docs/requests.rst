Requests
========

Request objects are passed to a Gateway object to perform an action or
retrieve some data from the Veritrans API.

All of these objects inherit from the RequestEntity mixin class and have
the ability to return a dictionary representation of themselves (later used
by the gateway to create the JSON body for a request), and also have the
ability to perform some validation of their attribute values (so time isn't
wasted submitting an HTTP request to the Veritrans API only to discover that
some of your input data was invalid).

ChargeRequest
-------------

A charge request is a container for information about a charge submitted
for a given customer.


.. autoclass:: veritranspay.request.ChargeRequest
    :members:
    :show-inheritance:

Sub Entities
------------

Subentities are logically smaller components that are used to generate
a request.


.. automodule:: veritranspay.request
   :members:
   :show-inheritance:

.. automodule:: veritranspay.payment_types
   :members:

Mixins
------
