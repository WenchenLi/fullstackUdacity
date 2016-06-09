# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Find these values at https://twilio.com/user/account
account_sid = "AC163b5848915cba329f04e5c8b153bd00"
auth_token = "6cbd1d9889594d78f1d1c795ee85349f"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to="+19176649819", from_="+13479606750",
                                     body="Hello there!")
