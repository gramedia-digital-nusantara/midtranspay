'''
MidtransPay
-------

Client library for communicating with **VERSION 2** of the
midtrans.co.id payment gateway.  Note, there is no support for the older
v1 API as this was dropped in Dec 2014.

Notes
`````
This is still an early release and does not provide access to all the
functionality of the Midtrans.co.id API.  Currently, only submitting
credit-card payments, and receiving that response is supported.

Links
`````

* `midtrans website <http://midtrans.co.id/>`_

'''
from setuptools import setup


pkg_req = [
    'requests>=2.3.0',
]
test_req = pkg_req + [
    'fake-factory>=0.4.2',
    'mock>=1.0.1',
    'nose>=1.3.4',
    'coverage>=3.7.1',
]


setup(
    name='MidtransPay',
    version=__import__('midtranspay').__version__,
    url='https://github.com/derekjamescurtis/midtranspay',
    license='BSD',
    author='Derek J. Curtis',
    author_email='derek.curtis@apps-foundry.com',
    description='Midtrans.co.id API Client Library ',
    long_description=__doc__,
    packages=['midtranspay',
              'midtranspay.response',
              ],
    include_package_data=True,
    platforms='any',
    classifiers=['Development Status :: 3 - Alpha',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 ],
    install_requires=pkg_req,
    tests_require=test_req,
    test_suite='nose.collector'
    )
