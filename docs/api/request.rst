Requests
========

Request objects are passed to a Gateway object to perform an action or
retrieve some data from the Veritrans API.

Request Types
-------------

.. autoclass:: veritranspay.request.ChargeRequest
    :members:
    :show-inheritance:

.. autoclass:: veritranspay.request.StatusRequest
    :members:
    :show-inheritance:

.. autoclass:: veritranspay.request.ApprovalRequest
    :members:
    :show-inheritance:

.. autoclass:: veritranspay.request.CancelRequest
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

.. automodule:: veritranspay.payment_types
    :members:
    :show-inheritance:

Others
^^^^^^

.. note::
    These have no use beyond building a 
    :py:class:`veritranspay.request.ChargeRequest`.

.. autoclass:: veritranspay.request.Address
    :members:
    :show-inheritance:

.. autoclass:: veritranspay.request.CustomerDetails
    :members:
    :show-inheritance:

.. autoclass:: veritranspay.request.TransactionDetails
    :members:
    :show-inheritance:

.. autoclass:: veritranspay.request.ItemDetails
    :members:
    :show-inheritance:
