# Veritrans VT-Direct API v2 Helper Library

A Python Helper library for communicating with the Veritrans Payment Gateway.

[![Build Status](https://travis-ci.org/derekjamescurtis/veritranspay.svg?branch=master)](https://travis-ci.org/derekjamescurtis/veritranspay)

[![Documentation Status](https://readthedocs.org/projects/veritranspay/badge/?version=latest)](https://readthedocs.org/projects/veritranspay/?badge=latest)


## Current Support

__NORMAL__ Credit Card charges via VT-Direct.

## Roadmap

Add support for additional payment methods.

- VT-Direct
    - Credit Cards
        - 3D Secure
    - Mandiri ClickPay
    - CIMB Clicks
    - Permata Virtual Account

Add support for additional VT-Direct commands.

- Check Transaction Status
- Approve Transaction
- Cancel Transaction


## Note

At the current time, this API is only tailored to making 
Credit Card requests to the Veritrans V2 API via VT-Direct.

There is no support at the current time for **anything** beyond that.


## Disclaimer

This software is **not** provided by or in any way associated
with or endorsed by PT. Midtrans (Veritrans Indonesia).  It is
a 3rd party library to ease communication with the Veritrans API
from Python Code.

It is entirely USE AT YOUR OWN RISK.

Read the license and documentation for full details.