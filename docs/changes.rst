Changes
=======

0.5
---

You can now query the API for information about previous transactions,
and cancel/approve transactions that are currently flagged as 'CHALLENGE'
from the midtrans fraud detection system.

**Added**

- :py:func:`midtranspay.midtrans.VTDirect.submit_status_request`
- :py:func:`midtranspay.midtrans.VTDirect.submit_approval_request`
- :py:func:`midtranspay.midtrans.VTDirect.submit_cancel_request`

**Changed**

- :py:func:`midtranspay.midtrans.VTDirect.submit_charge_request`
    - renamed param 'charge_req' to 'req'