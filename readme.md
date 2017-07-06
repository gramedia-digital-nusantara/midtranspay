# Midtranspay

[![Build Status](https://travis-ci.org/derekjamescurtis/midtranspay.svg?branch=master)](https://travis-ci.org/derekjamescurtis/midtranspay)
[![Documentation Status](https://readthedocs.org/projects/midtranspay/badge/?version=latest)](https://readthedocs.org/projects/midtranspay/?badge=latest)
[![Latest Version](https://img.shields.io/pypi/v/MidtransPay.svg)](https://pypi.python.org/pypi/MidtransPay/)
[![License](https://img.shields.io/pypi/l/MidtransPay.svg)](https://pypi.python.org/pypi/MidtransPay/)
[![Download format](https://img.shields.io/pypi/format/MidtransPay.svg)](https://pypi.python.org/pypi/MidtransPay/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/MidtransPay.svg)](https://pypi.python.org/pypi/MidtransPay/)
[![Downloads](https://img.shields.io/pypi/dm/MidtransPay.svg)](https://pypi.python.org/pypi/MidtransPay/)

A Python client library for communicating with the [Midtrans Payment Gateway](http://midtrans.co.id/).

Also, absolutely EVERYTHING in the API is subject to change in early release
versions (at least until 1.0), so make sure you have a good test suite
before upgrading versions!

Previous release versions will be maintained on PyPi, so make sure however
you're specifying your requirements, that you're using an exact version and
not just pulling the latest!

If you're needing a specific feature, feel free to submit a new issue, or
even better, a pull request!  Before submitting code though, make sure it
includes tests and documentation!


## Current Support (version 0.7)

- Submit Credit Card Charges (VTDirect)

- Python Versions
    - 2.7
    - 3.3
    - 3.4
- VT-Direct
    - Credit Cards
        - 3D Secure
        - One-Click
        - Two-Click
        - Indomaret
    - Request Transaction Status
    - Cancel Transaction
    - Approve Challenged Transaction

## Roadmap

Add support for additional payment methods.

- VT-Direct
    - Mandiri ClickPay
    - CIMB Clicks
    - Permata Virtual Account


## Links

- [Project on PyPi](https://pypi.python.org/pypi/MidtransPay)
- [ReadTheDocs](http://midtranspay.readthedocs.org/en/latest/)
- [Travis CI](https://travis-ci.org/derekjamescurtis/midtranspay)
- [Midtrans Indonesia](http://midtrans.co.id)


## Disclaimer

This software is **not** provided by or in any way associated
with or endorsed by PT. Midtrans (Midtrans Indonesia).  It is
a 3rd party library to ease communication with the Midtrans API
from Python Code.

It is entirely USE AT YOUR OWN RISK.

Read the license and documentation for full details.


## Acknowledgements

This project has been open sourced with the gracious permission of my
employer -- [Apps Foundry PTE LTD](http://apps-foundry.com).

My employer makes no assertions about the fitness of this software.
It is 100% entirely USE AT YOUR OWN RISK.
