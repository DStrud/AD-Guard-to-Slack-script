import json
import time
import requests

def send_slack_message(token, channel, text):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'channel': channel, 'text': text}
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print("Error sending message to Slack:", response.status_code, response.text)
    else:
        print("Message sent to Slack:", response.json())


def search_log_file(file_path, keywords, slack_token, slack_channel):
    last_position = 0
    while True:
        with open(file_path, 'r') as file:
            file.seek(last_position)
            new_lines = file.readlines()
            last_position = file.tell()

        found = False
        for line in new_lines:
            try:
                entry = json.loads(line)
                for keyword in keywords:
                    if keyword in json.dumps(entry):
                        message = f"Keyword '{keyword}' found in entry: {entry}"
                        print(message)
                        send_slack_message(slack_token, slack_channel, message)
                        found = True
            except json.JSONDecodeError:
                continue

        if not found and new_lines:
            print("No new keywords found in the recent entries.")

        time.sleep(10)

# Example usage
log_file_path = r'C:\AdGuardHome\data\querylog.json'
keywords_to_search = ['facebook', 'twitter']
slack_token = 'token'  # Replace with your Slack bot token
slack_channel = 'channel ID'  # Replace with your Slack channel ID
search_log_file(log_file_path, keywords_to_search, slack_token, slack_channel)