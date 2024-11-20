import smpp

# Define SMPP parameters
host = '10.26.142.160'
port = 5016
system_id = 'DOIT'
password = 'D01t4321'
source_addr = 'DOITbulk'  # This is the sender ID you mentioned

# Define destination phone number
destination_addr = '9844955757'

# Message content
message_content = 'Hello, this is a test message.'

# Establish SMPP connection
client = smpp.SMPPClient(host, port)

try:
    # Bind to SMSC
    client.bind(system_id, password)

    # Send SMS
    client.sendSMS(
        source_addr,
        destination_addr,
        message_content,
        source_addr_ton=1,  # Type of Number (TON) for sender (default is international)
        source_addr_npi=1,  # Numbering Plan Indicator (NPI) for sender (default is ISDN/telephone numbering plan)
        dest_addr_ton=1,    # TON for recipient (default is international)
        dest_addr_npi=1     # NPI for recipient (default is ISDN/telephone numbering plan)
    )

    print("Message sent successfully.")

except smpp.SMPPClientError as e:
    print("SMPP Client Error:", e)

finally:
    # Unbind from SMSC and close connection
    client.unbind()
    client.disconnect()
