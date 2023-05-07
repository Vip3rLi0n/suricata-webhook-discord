# Author: Vip3rLi0n

import time
import requests

WEBHOOK_URL = 'https://discord.com/api/webhooks/yourwebhookhere/changethislink'
LOG_FILE = '/var/log/suricata/fast.log'

# Initialize variables
counter = 0
last_line = ''

while True:
    with open(LOG_FILE, 'r') as f:
        # Read the last line in the file
        lines = f.read().splitlines()
        new_last_line = lines[-1] if lines else ''
        
        # Send a message if the last line has changed
        if new_last_line != last_line:
            last_line = new_last_line
            
            # Send message to Discord webhook
            payload = {
                'embeds': [{
                    'title': 'Suricata Alert',
                    'description': last_line,
                    'color': 0xffff00
                }],
                'username': 'Suricata Notification'
            }
            requests.post(WEBHOOK_URL, json=payload)
            
            # Reset the counter and send a message to Discord
            if counter >= 100:
                counter = 0
                payload = {
                    'embeds': [{
                        'title': 'Suricata Alert',
                        'description': 'System restored, Suricata are now running normally.',
                        'color': 0xffff00
                    }],
                    'username': 'Suricata Notification'
                }
                requests.post(WEBHOOK_URL, json=payload)
            
            # Reset the counter
            counter = 0
        
        # Increment the counter
        counter += 1
        
        # Send a warning message if there have been no updates for 100 tries
        if counter >= 100:
            payload = {
                'embeds': [{
                    'title': 'Suricata Alert',
                    'description': 'The log does not have any updates, please check the system!',
                    'color': 0xffff00
                }],
                'username': 'Suricata Notification'
            }
            requests.post(WEBHOOK_URL, json=payload)
            
    # Wait for 3 seconds before checking again
    time.sleep(3)
