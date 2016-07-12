from faker import Faker
fake = Faker()


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
        "order_id": "".join([fake.random_letter() for _ in range(10)]),
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

CC_CHARGE_RESPONSE_SUCCESS = {
    "transaction_id": "1a1a66f7-27a7-4844-ba1f-d86dcc16ab27",
    "order_id": "C17550",
    "gross_amount": "145000.00",
    "payment_type": "credit_card",
    "transaction_time": "2014-08-24 15:39:22",
    "transaction_status": "capture",
    "fraud_status": "accept",
    "masked_card": "481111-1114",
    "status_code": "200",
    "status_message": "Success, Credit Card 3D Secure "
                      "transaction is successful",
    "approval_code": "1408869563148"
}

CC_CHARGE_RESPONSE_FAIL = {
    "transaction_id": "b98fafec-fc2b-436f-bc6d-87853291cb35",
    "order_id": "C17550",
    "gross_amount": "145000.00",
    "payment_type": "credit_card",
    "transaction_time": "2014-08-24 15:44:15",
    "transaction_status": "deny",
    "fraud_status": "accept",
    "masked_card": "491111-1113",
    "status_code": "202",
    "status_message": "Deny by Bank [BNI] with code [05] "
                      "and message [Do not honour]"
}

INDOMARET_CHARGE_RESPONSE_SUCCESS = {
    "status_code": "201",
    "status_message": "Success, CSTORE transaction is successful",
    "transaction_id": "ff05337c-6c94-4f70-8e81-35acd89b688e",
    "order_id": "201404141421",
    "payment_type": "cstore",
    "transaction_time": "2014-04-14 16:03:51",
    "transaction_status": "pending",
    "payment_code": "498112345234",
    "gross_amount": "145000.00"
}

STATUS_RESPONSE = {
    "status_code": "200",
    "status_message": "Success, transaction found",
    "transaction_id": "e3b8c383-55b4-4223-bd77-15c48c0245ca",
    "masked_card": "481111-1114",
    "order_id": "2014112112",
    "payment_type": "credit_card",
    "transaction_time": "2014-11-21 13:07:50",
    "transaction_status": "settlement",
    "fraud_status": "accept",
    "approval_code": "1416550071152",
    "signature_key":
        "4ef8218aad5b64bae2ec9d6b0f0a0b059b88bd298f9e79e662f641b"
        "ae7cd24992fb67547ea60cc3f9a820ca7e5649cf5e1"
        "f0a8e4b5ef24001f951b7a9d1a8f42",
    "bank": "mandiri",
    "gross_amount": "10000.00"
}

APPROVE_RESPONSE = {
    "status_code": "200",
    "status_message": "Success, transaction is approved",
    "transaction_id": "2af158d4-b82e-46ac-808b-be19aaa96ce3",
    "masked_card": "451111-1117",
    "order_id": "2014112112",
    "payment_type": "credit_card",
    "transaction_time": "2014-11-27 10:05:10",
    "transaction_status": "capture",
    "fraud_status": "accept",
    "approval_code": "1417057511311",
    "bank": "bni",
    "gross_amount": "10000.00"
}

CANCEL_RESPONSE = {
    "status_code": "200",
    "status_message": "Success, transaction is canceled",
    "transaction_id": "2af158d4-b82e-46ac-808b-be19aaa96ce3",
    "masked_card": "451111-1117",
    "order_id": "2014112112",
    "payment_type": "credit_card",
    "transaction_time": "2014-11-27 10:05:10",
    "transaction_status": "cancel",
    "fraud_status": "accept",
    "bank": "bni",
    "gross_amount": "10000.00"
}
