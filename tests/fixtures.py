PHONE_NUMBERS = ('+62 812 1272 8059',
                 '+1 (330) 776-8177',
                 '81212728059',
                 )

COUNTRY_CODES = ('USA',
                 'IDN',
                 'SIN',
                 )


TOKEN_ID = 'i-am-a-fake-token'


# Testing Cards
# http://docs.veritranspay.co.id/sandbox/card_list.html
CC_ACCEPTED = ['4011 1111 1111 1112',
               '5481 1611 1111 1081',
               ]
CC_CHALLENGED_FDS = ['4111 1111 1111 1111',
                     '5110 1111 1111 1119',
                     ]
CC_DENY_FDS = ['4211 1111 1111 1110',
               '5210 1111 1111 1118',
               ]
CC_DENY_BANK = ['4311 1111 1111 1119',
                '5310 1111 1111 1117',
                ]
CC_CVV = '123'
CC_EXPIRY_MONTH = '01'
CC_EXPIRY_YEAR = '2020'


# These examples are pulled straight from the Veritrans documentation
# http://docs.veritranspay.co.id/sandbox/charge.html#the-structure-and-example-of-json-response-vt-direct-using-credit-card
CC_REQUEST = {
    "payment_type": "credit_card",
    "credit_card": {
        "bank": "bni",
        "token_id": TOKEN_ID
    },
    "transaction_details": {
        "order_id": "C17550",
        "gross_amount": 145000
    },
    "customer_details": {
        "first_name": "Andri",
        "last_name": "Litani",
        "email": "andri@litani.com",
        "phone": "081122334455",
        "billing_address": {
            "first_name": "Andri",
            "last_name": "Litani",
            "address": "Mangga 20",
            "city": "Jakarta",
            "postal_code": "16602",
            "phone": "081122334455",
            "country_code": "IDN"
        },
        "shipping_address": {
            "first_name": "Obet",
            "last_name": "Supriadi",
            "address": "Manggis 90",
            "city": "Jakarta",
            "postal_code": "16601",
            "phone": "08113366345",
            "country_code": "IDN"
        }
    },
    "item_details": [
        {
            "id": "a1",
            "price": 50000,
            "quantity": 2,
            "name": "Apel"
        },
        {
            "id": "a2",
            "price": 45000,
            "quantity": 1,
            "name": "Jeruk"
        }
    ]
}

RESPONSE_SUCCESS = {
    "transaction_id": "1a1a66f7-27a7-4844-ba1f-d86dcc16ab27",
    "order_id": "C17550",
    "gross_amount": "145000.00",
    "payment_type": "credit_card",
    "transaction_time": "2014-08-24 15:39:22",
    "transaction_status": "capture",
    "fraud_status": "accept",
    "masked_card": "481111-1114",
    "status_code": "200",
    "status_message": "Success, Credit Card 3D Secure transaction is successful",
    "approval_code": "1408869563148"
}

RESPONSE_FAIL = {
    "transaction_id": "b98fafec-fc2b-436f-bc6d-87853291cb35",
    "order_id": "C17550",
    "gross_amount": "145000.00",
    "payment_type": "credit_card",
    "transaction_time": "2014-08-24 15:44:15",
    "transaction_status": "deny",
    "fraud_status": "accept",
    "masked_card": "491111-1113",
    "status_code": "202",
    "status_message": "Deny by Bank [BNI] with code [05] and message [Do not honour]"
}
