'''
VeritransPay
-------

This is a helper library for communicating with **VERSION 2** of the
veritrans.co.id payment gateway.  Note, there is no support for the older
v1 API as this is being dropped around Dec 2014.

Notes
`````
This is still an early release and does not provide access to all the
functionality of the Veritrans.co.id API.  Currently, only submitting
credit-card payments, and receiving that response is supported.

Links
`````

* `veritrans website <http://veritrans.co.id/>`_

'''
from setuptools import setup


pkg_req = [
    'requests>=2.3.0',
]
test_req = pkg_req + [
    'fake-factory>=0.4.2',
    'mock>=1.0.1',
    'nose>=1.3.4',
]


setup(
    name='VeritransPay',
    version=__import__('veritranspay').__version__,
    url='https://github.com/derekjamescurtis/veritranspay',
    license='BSD',
    author='Derek J. Curtis',
    author_email='derek.curtis@apps-foundry.com',
    description='Veritrans.co.id API v2 Helper Library ',
    long_description=__doc__,
    packages=['veritranspay',
              'veritranspay.response',
              ],
    include_package_data=True,
    platforms='any',

    install_requires=pkg_req,
    tests_require=test_req,

    )
