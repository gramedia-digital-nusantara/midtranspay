
POSTALCODE_REQUIRED = r'^([\d -]{1,10})$'
NAME_OPTIONAL = r'^(.{0,20})$'
NAME_REQUIRED = r'^(.{1,20})$'

# e-mails are actually complicated to validate.. since we're doing a simple
# validator, we're just going to worry about the length.
EMAIL_OPTIONAL = r'^.{0,45}$'
EMAIL_REQUIRED = r'^.{1,45}$'

PHONE_OPTIONAL = r'^([\d\+\-\(\) ]{5,19})$|^$'
PHONE_REQUIRED = r'^([\d\+\-\(\) ]{5,19})$'

DUMMY_VALIDATOR = ''
