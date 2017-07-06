Gateways
========

Gateway objects are used to submit requests, and receive back responses
from the Midtrans API.

When the gateway is created, by default, it is set to production mode,
however you can specify that a gateway should run in sandbox mode
by passing the appropriate value to it's __init__() method.

.. note::
    Currently, only the VT-Direct gateway is supported.

.. automodule:: midtranspay.midtrans
    :members:
    :show-inheritance: