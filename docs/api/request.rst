Requests
========

Request objects are passed to a Gateway object to perform an action or
retrieve some data from the Midtrans API.

Request Types
-------------

.. autoclass:: midtranspay.request.ChargeRequest
    :members:
    :show-inheritance:

.. autoclass:: midtranspay.request.StatusRequest
    :members:
    :show-inheritance:

.. autoclass:: midtranspay.request.ApprovalRequest
    :members:
    :show-inheritance:

.. autoclass:: midtranspay.request.CancelRequest
    :members:
    :show-inheritance:

Sub Entities
------------

Subentities are logically smaller components that are used to generate
a request.  Currently, sub-entities are only used when making a ChargeRequest.

Payment Types
^^^^^^^^^^^^^

.. warning::
    At the current time **ONLY** Credit Card payments are supported.

.. automodule:: midtranspay.payment_types
    :members:
    :show-inheritance:

Others
^^^^^^

.. note::
    These have no use beyond building a 
    :py:class:`midtranspay.request.ChargeRequest`.

.. autoclass:: midtranspay.request.Address
    :members:
    :show-inheritance:

.. autoclass:: midtranspay.request.CustomerDetails
    :members:
    :show-inheritance:

.. autoclass:: midtranspay.request.TransactionDetails
    :members:
    :show-inheritance:

.. autoclass:: midtranspay.request.ItemDetails
    :members:
    :show-inheritance:
