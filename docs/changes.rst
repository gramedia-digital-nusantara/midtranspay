Changes
=======

0.5
---

You can now query the API for information about previous transactions,
and cancel/approve transactions that are currently flagged as 'CHALLENGE'
from the veritrans fraud detection system.

**Added**

- :py:func:`veritranspay.veritrans.VTDirect.submit_status_request`
- :py:func:`veritranspay.veritrans.VTDirect.submit_approval_request`
- :py:func:`veritranspay.veritrans.VTDirect.submit_cancel_request`

**Changed**

- :py:func:`veritranspay.veritrans.VTDirect.submit_charge_request`
    - renamed param 'charge_req' to 'req'