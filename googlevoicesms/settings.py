DEFAULT_CONFIG = """
[auth]
# Google Account email address (one associated w/ your Voice account)
email=

# Raw password used or login
password=

[gvoice]
# Number to place calls from (eg, your google voice number)
forwardingNumber=

# Default phoneType for your forwardingNumber as defined below
#  1 - Home
#  2 - Mobile
#  3 - Work
#  7 - Gizmo
phoneType=2
"""

DEBUG = False
LOGIN = 'https://accounts.google.com/ServiceLogin?service=grandcentral'
FEEDS = ('sms')

BASE = 'https://www.google.com/voice/'
LOGOUT = BASE + 'account/signout'
INBOX = BASE + '#inbox'
SMS = BASE + 'sms/send/'

XML_SEARCH = BASE + 'inbox/search/'
XML_RECENT = BASE + 'inbox/recent/'
XML_SMS = XML_RECENT + 'sms/'
