# DEPRECATED Veritranspay 

[![Build Status](https://travis-ci.org/derekjamescurtis/veritranspay.svg?branch=master)](https://travis-ci.org/derekjamescurtis/veritranspay)
[![Documentation Status](https://readthedocs.org/projects/veritranspay/badge/?version=latest)](https://readthedocs.org/projects/veritranspay/?badge=latest)
[![Latest Version](https://img.shields.io/pypi/v/VeritransPay.svg)](https://pypi.python.org/pypi/VeritransPay/)
[![License](https://img.shields.io/pypi/l/VeritransPay.svg)](https://pypi.python.org/pypi/VeritransPay/)
[![Download format](https://img.shields.io/pypi/format/VeritransPay.svg)](https://pypi.python.org/pypi/VeritransPay/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/VeritransPay.svg)](https://pypi.python.org/pypi/VeritransPay/)
[![Downloads](https://img.shields.io/pypi/dm/VeritransPay.svg)](https://pypi.python.org/pypi/VeritransPay/)


## Notice

Midtrans has released an (officially-supported python client)[https://github.com/Midtrans/midtrans-python-client].  We recommend migrating to that library as soon as practical, as midtranspay has not been updated or supported in quite some time.

## Overview

A Python client library for communicating with the [Veritrans Payment Gateway](http://veritrans.co.id/).

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

- [Project on PyPi](https://pypi.python.org/pypi/VeritransPay)
- [ReadTheDocs](http://veritranspay.readthedocs.org/en/latest/)
- [Travis CI](https://travis-ci.org/derekjamescurtis/veritranspay)
- [Veritrans Indonesia](http://veritrans.co.id)


## Disclaimer

This software is **not** provided by or in any way associated
with or endorsed by PT. Midtrans (Veritrans Indonesia).  It is
a 3rd party library to ease communication with the Veritrans API
from Python Code.

It is entirely USE AT YOUR OWN RISK.

Read the license and documentation for full details.


## Acknowledgements

This project has been open sourced with the gracious permission of my
employer -- [Apps Foundry PTE LTD](http://apps-foundry.com).

My employer makes no assertions about the fitness of this software.
It is 100% entirely USE AT YOUR OWN RISK.
