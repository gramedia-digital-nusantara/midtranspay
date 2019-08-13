'''
VeritransPay
------------

Client library for communicating with **VERSION 2** of the
veritrans.co.id payment gateway.  Note, there is no support for the older
v1 API as this was dropped in Dec 2014.

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
    'coverage>=3.7.1',
]


setup(
    name='VeritransPay',
    version=__import__('veritranspay').__version__,
    url='https://github.com/derekjamescurtis/veritranspay',
    license='BSD',
    author='Derek J. Curtis',
    author_email='derek.curtis@apps-foundry.com',
    description='Veritrans.co.id API Client Library ',
    long_description=__doc__,
    packages=['veritranspay',
              'veritranspay.response',
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
